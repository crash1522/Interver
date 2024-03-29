from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.answer import answer_crud
from domain.user.user_router import get_current_user
from domain.feedback import feedback_schema, feedback_crud
from models import User

router = APIRouter(
    prefix="/api/feedback",
)


@router.post("/create/{answer_id}", response_model=feedback_schema.Feedback)
def feedback_create(answer_id: int,
                  _feedback_create: feedback_schema.FeedbackCreate,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):

    # create answer
    answer = answer_crud.get_answer(db, answer_id=answer_id)
    if not answer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found.")
    feedback = feedback_crud.create_feedback(db, answer=answer,
                              feedback_create=_feedback_create)
    return feedback

@router.get("/detail/{feedback_id}", response_model=feedback_schema.Feedback)
def feedback_detail(feedback_id: int, db: Session = Depends(get_db)):
    feedback = feedback_crud.get_feedback(db, feedback_id=feedback_id)
    if not feedback:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found.")
    return feedback


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def feedback_delete(_feedback_delete: feedback_schema.FeedbackDelete,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_feedback = feedback_crud.get_feedback(db, feedback_id=_feedback_delete.feedback_id)
    if not db_feedback:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    feedback_crud.delete_feedback(db=db, db_feedback=db_feedback)