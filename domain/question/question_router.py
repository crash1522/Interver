from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from domain.question import question_schema, question_crud
from domain.answer import answer_crud
from domain.user import user_router, user_schema
from domain.record import record_crud
from common.agent import agent_dict
from common.handler.handler_router import q_cnt_dict
from models import User
from database import get_db

router = APIRouter(
    prefix="/api/question",
)

@router.post("/question_create/{record_id}", response_model = question_schema.Question)
async def question_create(record_id: int,
                         before_answer_id: Optional[int]=None,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(user_router.get_current_user)):
    global agent_dict, q_cnt_dict
    try:
        conversational_agent_executor = agent_dict[record_id]
    except:
        raise HTTPException(status_code=404, detail=f"Not Valid record id (record id: {record_id})")

    if not before_answer_id:
        # 초기 프롬프트 설정, 추후 소령님 작업물로 변환
        # input_dict 이용
        # 초기 프롬프트 설정 이후 해당 키값 삭제
        greeting = f"안녕하세요, {current_user.field} 직군에 지원한 홍길동입니다."
        chat_response  = await conversational_agent_executor.ainvoke(
            {"input": greeting},
             config={"configurable":{"user_id":current_user.id, "conversation_id":record_id}},
        )
    else:
        before_answer = answer_crud.get_answer(db=db, answer_id=before_answer_id)
        user_answer = before_answer.content
    
        # 챗봇으로부터 다음 면접 질문을 받아옴
        chat_response = await conversational_agent_executor.ainvoke(
            {"input": user_answer},  # 사용자의 면접 대답 전달
            config={"configurable":{"user_id":current_user.id, "conversation_id":record_id}},
        )
    if chat_response:
        new_question_content = chat_response
        new_question = question_crud.create_question(db=db,
                                                     question_create=question_schema.QuestionCreate(content = new_question_content),
                                                     record_id=record_id)
        q_cnt_dict[record_id].cur_question_num += 1   
        return new_question
    else:
        raise HTTPException(status_code=500, detail="Failed to receive a new question from the chatbot")



"""
# 인자로 입력값들 받아야함 (입력 페이지)
@router.post("/first-question", response_model = question_schema.Question)
async def first_question(
        company_info: handler_schema.CompanyInfo,
        cover_letter: handler_schema.CoverLetter,
        db: Session = Depends(get_db), 
        current_user: user_schema.User = Depends(user_router.get_current_user)):
    new_record = record_crud.create_record(db, current_user)
    greeting = f"안녕하세요, AI개발에 지원한 {current_user.username}입니다."
    
    # 회사 정보, 자기소개서도 입력받아야함, 현재는 default값들어가고 있음
    new_input = handler.input_create(db=db, user=current_user, company_info=company_info, cover_letter=cover_letter)

    # 새로운 agent 생성 후, 메모리에 저장
    new_agent = agent.create_agent(new_input)
    agent_dict[new_record.id] = new_agent

    # 챗봇으로부터 다음 면접 질문을 받아옴
    chat_response  = await new_agent.ainvoke(
        {"input": greeting},
        {"configurable": {"session_id": new_record.id}},
    )
    # 챗봇 응답 검증 및 데이터베이스에 저장
    if chat_response and chat_response.get("output"):
        first_question = chat_response.get("output")
    else:
        # 적절한 오류 처리 또는 기본값 할당
        first_question = "다음 질문을 준비 중입니다."

    # 여기서 첫 번째 면접 질문에 해당하는 `first_question`을 사용하여 새로운 질문 인스턴스를 생성하고 저장
    new_question = question_crud.create_question(db=db,
                                                 question_create=question_schema.QuestionCreate(content = first_question),
                                                 record_id=new_record.id)
    return new_question

@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = question_crud.get_question(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Question not found.")
    return question


@router.post("/create/{record_id}", response_model=question_schema.Question)
def question_create(_question_create: question_schema.QuestionCreate,
                    record_id: int,
                    db: Session = Depends(get_db),):
    question = question_crud.create_question(db=db, question_create=_question_create, record_id=record_id)
    return question


@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def question_update(_question_update: question_schema.QuestionUpdate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(user_router.get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_update.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    question_crud.update_question(db=db, db_question=db_question,
                                  question_update=_question_update)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def question_delete(_question_delete: question_schema.QuestionDelete,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(user_router.get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_delete.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    question_crud.delete_question(db=db, db_question=db_question)


# async examples 
@router.post("/async_create", status_code=status.HTTP_204_NO_CONTENT)
async def async_question_create(_question_create: question_schema.QuestionCreate,
                                db: Session = Depends(get_async_db)):
    await question_crud.async_create_question(db, question_create=_question_create)
"""