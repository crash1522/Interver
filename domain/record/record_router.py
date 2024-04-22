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
from database import get_db

router = APIRouter(
    prefix="/api/record",
)


@router.get("/create")
def record_create(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> int:
    record = record_crud.create_record(db=db, user=current_user)
    if not record:
        raise HTTPException(status_code=500, detail=f"Record doesn't be created.")
    return record.id


"""
    현재 백그라운드에서 실행 중인 feedback 생성이 모두 실행되기 전에 요청을 날려서 feedback에 None이 담김
    feedback이라서 js에서 랜더링 안하는 것으로 보임
"""
@router.get("/detail/{record_id}")
def record_detail(record_id: int, db: Session = Depends(get_db)):
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