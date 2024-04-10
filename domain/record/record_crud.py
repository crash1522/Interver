from sqlalchemy.orm import Session
from datetime import datetime

from domain.record.record_schema import Record
from domain.user import user_crud 
from models import User, Record, Question, Answer, Feedback


def get_record(db: Session, record_id: int):
    record = db.query(Record).filter(Record.id == record_id).first()
    return record


def get_all_data_by_record_id(db: Session, record_id: int):
    questions = db.query(Question).filter(Question.record_id == record_id).all()
    answers = []
    feedbacks = []
    for question in questions:
        answer = db.query(Answer).filter(Answer.question_id==question.id).first()
        answers.append(answer)
        if answer:
            feedback = db.query(Feedback).filter(Feedback.answer_id==answer.id).first()
            feedbacks.append(feedback)
        else:
            feedbacks.append(None)

    return questions, answers, feedbacks


def create_record(db: Session, user: User):
    db_record= Record(
        user_id=user_crud.get_id(db=db,userid=user.userid),
        create_date=datetime.now())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)  # 생성된 질문 인스턴스를 최신 상태로 업데이트
    return db_record


def delete_record(db: Session, db_record: Record):
    db.delete(db_record)
    db.commit()