from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page, add_pagination, paginate
from sqlalchemy.orm import Session
from sqlalchemy import select
from starlette import status

from database import get_db
from domain.record import record_crud, record_schema
from domain.user import user_crud
from domain.user.user_router import get_current_user
from domain.question.question_crud import delete_question
from domain.answer.answer_crud import delete_answer
from domain.feedback.feedback_crud import delete_feedback
from models import User, Record

router = APIRouter(
    prefix="/api/record",
)

"""
@router.post("/create", response_model=record_schema.Record)
def record_create(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    record = record_crud.create_record(db=db, user=current_user)
    return record
"""

@router.get("/detail/{record_id}")
def record_detail(record_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    record = record_crud.get_record(db, record_id=record_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Record is not found.")
    
    questions, answers, feedbacks = record_crud.get_all_data_by_record_id(db, record_id=record_id)
    return {
        "record": record,
        "questions": questions,
        "answers": answers,
        "feedbacks": feedbacks
        }


# record 저장소에 페이지네이션 적용
@router.get('/get_records')
def get_records(user: User = Depends(get_current_user), 
                db: Session = Depends(get_db)) -> Page[record_schema.Record]:
    records = user_crud.get_records_by_userid(db=db, userid=user.userid)
    return paginate(records)

"""
input: @@@@@

when: @@@@
then: @@@@

when: @@@
then: @@@@@
"""
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
        delete_question(db, db_question=question)
    for answer in answers:
        delete_answer(db, db_answer=answer)
    for feedback in feedbacks:
        delete_feedback(db, db_feedback=feedback)

    # 레코드를 삭제합니다 
    record_crud.delete_record(db=db, db_record=db_record)
    
add_pagination(router)