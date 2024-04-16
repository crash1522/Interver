import os
from dotenv import load_dotenv
import logging
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.memory import ChatMessageHistory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler 
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables import ConfigurableFieldSpec

from common.handler import handler_schema
from typing import Dict
from openai import OpenAI

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY')
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')
llm = ChatOpenAI(api_key=OPENAI_API_KEY)
stt_llm = OpenAI(api_key=OPENAI_API_KEY)

### Save chat history
store = {}

agent_dict: Dict[int, RunnableWithMessageHistory] = {}

# 주어진 session_id에 대한 이력 반환
def get_session_history(user_id:str, conversation_id:str) -> BaseChatMessageHistory:
    # 해당 세션 ID가 저장소에 없다면, 새로운 ChatMessageHistory 인스턴스를 생성하여 저장소에 추가
    if (user_id, conversation_id) not in store:
        store[(user_id, conversation_id)] = ChatMessageHistory()
    return store[(user_id, conversation_id)]


def create_agent(new_input: handler_schema.Input):
    user_info = new_input.user_info
    company_info = new_input.company_info
    cover_letter = new_input.cover_letter

    ask_output_parser= StrOutputParser()
    essential_question = " 귀사에 지원하게 된 동기가 무엇인가요 ?"
    
        # JSON으로 직접 직렬화할 수 없는 복잡한 개체
    ask_prompt = ChatPromptTemplate.from_messages(
        [
<<<<<<< HEAD
            ("system",f"나는 지원자 역할을 하고, 당신은 면접관 역할을 한다. 우리는 {field} 포지션에 대한 면접을 진행한다. 우리의 역할은 변경되지 않는다. 면접 과정은 오로지 한국어로만 진행된다. 사용자가 설정한 {필수_질문}은 반드시 질문한다. 지원자의 자기소개서는 {cover_letter}이다. 회사의 요구사항은 {desired_candidate}이다. 자기소개서와 회사의 요구사항을 바탕으로 질문한다. 질문 할 때마다 반드시 몇 번째 질문인지 표시한다. 나의 답변을 기다린 후 다음 질문으로 넘어간다. 한번에 하나의 질문을 한다. 첫 질문은 반드시 지원동기를 묻는다. 설명이나 다른 형태의 대화는 제공하지 않는다."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
=======
            # 조건 요구
            ("system",f""" 너는 채용 면접관으로써 오직 질문만 한다. 나는 지원자이고 너의 질문에 대답을 할 것이다. 너는 {user_info.field} 직무에 관련한 질문을 할 것이다.
                            대화의 방식은 실제 면접과 동일하다. 너의 질문에 내가 대답을 하면 다음 질문으로 넘어간다.
                            지원자의 자기소개서는 {cover_letter.content}이다. 회사의 요구사항은 {company_info.prefered_qualification}이다. 사용자가 설정한 {essential_question}은 반드시 질문한다. 
                            {user_info.field} 분야의 5개의 기술 질문을 한다. 여기서 기술 질문이란 해당 분야하여 면접에서 자주 묻는 개념 관련 질문이다.
                            모든 질문은 자기소개서와 회사의 요구사항을 바탕으로 질문한다. 설명이나 다른 형태의 대화는 제공하지 않는다"""),
            MessagesPlaceholder(variable_name="history"),
            ("human","{input}"),
>>>>>>> feature/prompt_engineering
        ]
    )
    ## llm 객체 생성
    ask_llm = ChatOpenAI(temperature=1.0, # 창의성(0.0 ~ 2.0)
                max_tokens=2048, 
                model_name='gpt-4-0125-preview', 
                streaming=True,
                # 대화 시 특정 이벤트가 발생할 때, 실행할 콜백 함수 지정(일반적으로 비동기식으로 실행됨)
                callbacks=[StreamingStdOutCallbackHandler()]) # 대화 중 stdout을 streaming하는 작업 처리, 그 결과에 대한 콜백을 다룸

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

    conversational_agent_executor = RunnableWithMessageHistory(
        ask_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
        history_factory_config=[
            ConfigurableFieldSpec(
                id="user_id",
                annotation=str,
                name="User ID",
                description="Unique identifier for the user.",
                default="",
                is_shared=True,
            ),
            ConfigurableFieldSpec(
                id="conversation_id",
                annotation=str,
                name="Conversation ID",
                description="Unique identifier for the conversation.",
                default="",
                is_shared=True,
            ),
        ],
    )
    
    return conversational_agent_executor

