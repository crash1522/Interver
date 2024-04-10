import os
from dotenv import load_dotenv
import logging
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.memory import ConversationSummaryBufferMemory, ChatMessageHistory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.agents import AgentExecutor, create_openai_tools_agent

from common.handler import handler, handler_schema
from models import User

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
print(OPENAI_API_KEY)
LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY')
llm = ChatOpenAI(api_key=OPENAI_API_KEY)

ask_output_parser = StrOutputParser() #출력을 문자열로
ask_llm = ChatOpenAI(temperature=0,               # 창의성 (0.0 ~ 2.0) 
                 max_tokens=2048,             # 최대 토큰수
                 model_name='gpt-3.5-turbo',  # 모델명
                )
memory = ConversationSummaryBufferMemory(
    llm=ask_llm,
    max_token_limit=800,
    memory_key="chat_history",
    return_messages=True,
)


def create_agent(new_input: handler_schema.Input):
    user_info = new_input.user_info
    company_info = new_input.company_info
    field = user_info.field

    cover_letter = new_input.cover_letter
    필수_질문 = "최신 뉴스의 내용을 기반으로 한 질문"
    desired_candidate = company_info.desired_candidate 
    
    ask_prompt = ChatPromptTemplate.from_messages(
        [
            ("system",f"나는 지원자 역할을 하고, 당신은 면접관 역할을 한다. 우리는 {field} 포지션에 대한 면접을 진행한다. 우리의 역할은 변경되지 않는다. 면접 과정은 오로지 한국어로만 진행된다. 사용자가 설정한 {필수_질문}은 반드시 질문한다. 지원자의 자기소개서는 {cover_letter}이다. 회사의 요구사항은 {desired_candidate}이다. 자기소개서와 회사의 요구사항을 바탕으로 질문한다. 질문 할 때마다 반드시 몇 번째 질문인지 표시한다. 나의 답변을 기다린 후 다음 질문으로 넘어간다. 한번에 하나의 질문을 한다. 설명이나 다른 형태의 대화는 제공하지 않는다. 질문이 총 10개 제시되었을 때, 혹은 지원자가 '면접 종료'라고 말했을 때만 면접을 종료한다. 지원자가 면접 상황에 어울리지 않는 답변을 하거나 자기소개서의 내용과 맞지 않는 답변을 하면 지원자에게 경고한다. 경고가 2번 누적되면 대화를 종료한다."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    ask_chain = ask_prompt | ask_llm | ask_output_parser


    # 1. Load Retriever
    loader = WebBaseLoader("https://www.ttimes.co.kr/")
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings()
    vector = FAISS.from_documents(documents, embeddings)
    retriever = vector.as_retriever()

    # 2. Create Tools
    retriever_tool = create_retriever_tool(
        retriever,
        "news_search",
        "면접자의 직종과 관련된 최신 뉴스에 관하여 질문 할 때, 반드시 이 문서의 내용을 기반으로 질문한다.",
    )
    search = TavilySearchResults(k=2)
    tools = [retriever_tool, search]
    agent = create_openai_tools_agent(ask_llm, tools, ask_prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)
    demo_ephemeral_chat_history_for_chain = ChatMessageHistory()

    conversational_agent_executor = RunnableWithMessageHistory(
        agent_executor,
        lambda session_id: demo_ephemeral_chat_history_for_chain,
        input_messages_key="input",
        history_messages_key="chat_history",
    )
    return conversational_agent_executor

