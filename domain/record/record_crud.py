from sqlalchemy.orm import Session
from datetime import datetime

from domain.record.record_schema import Record
from models import User, Record, Question, Answer, Feedback


def get_record(db: Session, record_id: int):
    record = db.query(Record).filter(Record.id == record_id).first()
    return record


def get_all_data_by_record_id(db: Session, record_id: int):
    questions = db.query(Question).filter(Question.record_id == record_id).all()
    if not questions:
        return None
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

# nth_round 검증하기
def create_record(db: Session, user: User):
    # 특정 사용자의 기존 레코드 수 계산
    nth_round = db.query(Record).filter(Record.user_id == user.id).count() + 1

    # 새로운 레코드 생성
    db_record = Record(
        userid=user.userid,
        create_date=datetime.now())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)  # 생성된 레코드 인스턴스를 최신 상태로 업데이트
    return db_record

def delete_record(db: Session, db_record: Record):
    db.delete(db_record)
    db.commit()