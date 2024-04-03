from sqlalchemy.orm import Session

from domain.feedback.feedback_schema import FeedbackCreate
from models import Answer, Feedback


def create_feedback(db: Session, answer: Answer,
                  feedback_create: FeedbackCreate):
    db_feedback = Feedback(answer_id = answer.id,
                         content = feedback_create.content
                         )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def get_feedback(db: Session, feedback_id: int) -> Feedback:
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    return feedback


def get_feed_by_answer_id(db: Session, answer_id: int) -> Answer:
    return db.query(Feedback.answer_id==answer_id)


def delete_feedback(db: Session, db_feedback: Feedback):
    db.delete(db_feedback)
    db.commit()