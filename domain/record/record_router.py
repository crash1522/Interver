from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page, add_pagination, paginate
from sqlalchemy.orm import Session
from starlette import status

from domain.record import record_crud, record_schema
from domain.user import user_crud, user_schema
from domain.user.user_router import get_current_user
from domain.question import question_crud, question_schema
from domain.answer.answer_crud import delete_answer
from domain.feedback.feedback_crud import delete_feedback
from common.handler import handler_router, handler_schema
from common import agent
from common.agent import agent_dict
from models import User

router = APIRouter(
    prefix="/api/record",
)


@router.get("/create")
def record_create(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> int:
    record = record_crud.create_record(db=db, user=current_user)
    if not record:
        raise HTTPException(status_code=500, detail=f"Record doesn't be created.")
    return record.id


@router.get("/detail/{record_id}")
def record_detail(record_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    record = record_crud.get_record(db, record_id=record_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Record is not found.")
    
    questions, answers, feedbacks = record_crud.get_all_data_by_record_id(db, record_id=record_id)
    if not questions:
        raise HTTPException(status_code=404, detail=f"No questions found for this record.")
    return {
            "record": record,
            "questions": questions,
            "answers": answers,
            "feedbacks": feedbacks
        }
"""

# record 저장소에 페이지네이션 적용
@router.get('/get_records')
def get_records(user: User = Depends(get_current_user), 
                db: Session = Depends(get_db)) -> Page[record_schema.Record]:
    records = user_crud.get_records_by_userid(db=db, userid=user.userid)
    # records가 하나도 없을 경우 어떻게 나오고 있지?
    return paginate(records)


@router.post("/start_record", response_model = question_schema.Question)
async def start_record(company_info: handler_schema.CompanyInfo,
        cover_letter: handler_schema.CoverLetter,
        db: Session = Depends(get_db), 
        current_user: user_schema.User = Depends(get_current_user)):
    new_record = record_crud.create_record(db, current_user)
    greeting = f"안녕하세요, AI개발에 지원한 {current_user.username}입니다."
    
    # 회사 정보, 자기소개서도 입력받아야함, 현재는 default값들어가고 있음
    new_input = handler_router.input_create(db=db, user=current_user, company_info=company_info, cover_letter=cover_letter)

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




@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def record_delete(_record_delete: record_schema.RecordDelete,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_record = record_crud.get_record(db, record_id=_record_delete.record_id)
    
    if not db_record:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_record.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    
    # 해당 record에 담겨있는 모든 질문, 답변을 삭제합니다.
    questions, answers, feedbacks = record_crud.get_all_data_by_record_id(db, record_id=db_record.id)
    for question in questions:
        question_crud.delete_question(db, db_question=question)
    for answer in answers:
        delete_answer(db, db_answer=answer)
    for feedback in feedbacks:
        delete_feedback(db, db_feedback=feedback)

    # 레코드를 삭제합니다 
    record_crud.delete_record(db=db, db_record=db_record)
    
add_pagination(router)