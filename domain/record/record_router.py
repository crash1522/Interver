from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.record import record_crud, record_schema
from domain.user.user_router import get_current_user
from domain.question.question_crud import delete_question
from domain.answer.answer_crud import delete_answer
from domain.feedback.feedback_crud import delete_feedback
from models import User

router = APIRouter(
    prefix="/api/record",
)

"""
@router.post("/create", response_model=record_schema.Record)
def record_create(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    record = record_crud.create_record(db=db, user=current_user)
    return record
"""
@router.get("/detail/{userid}/{record_id}")
def record_detail(userid: str, record_id: int, db: Session = Depends(get_db)):
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
