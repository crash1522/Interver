from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

from database import Base

question_voter = Table(
    'question_voter',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('question_id', Integer, ForeignKey('question.id'), primary_key=True)
)

answer_voter = Table(
    'answer_voter',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('answer_id', Integer, ForeignKey('answer.id'), primary_key=True)
)

    
class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"))
    userid = Column(String, ForeignKey("user.userid"))
    
    question = relationship("Question", back_populates="answer", uselist=False)
    user = relationship("User", back_populates="answers")

class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    record_id = Column(Integer, ForeignKey("record.id"))

    answer = relationship('Answer', back_populates='question', uselist=False)
    record = relationship("Record", back_populates="questions")

class Record(Base):
    __tablename__ = "record"

    id = Column(Integer, primary_key=True)
    userid = Column(String, ForeignKey("user.userid"))
    create_date = Column(DateTime, nullable=False)
    
    user = relationship("User", back_populates="records")
    questions = relationship('Question', back_populates = "record")

    arbitrary_types_allowed=True

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    userid = Column(String, unique=True, nullable=False)
    username = Column(String, unique=False, nullable=False)
    password = Column(String, nullable=False)
    field = Column(String)

    skills = relationship("Skill", back_populates="user")
    records = relationship("Record", back_populates="user")
    answers = relationship("Answer", back_populates="user")
   
class Skill(Base):
    __tablename__ = "skill"
    
    id = Column(Integer, primary_key=True)
    skill_name = Column(String, nullable=False)
    userid = Column(String, ForeignKey('user.userid'), nullable=False)

    user = relationship("User", back_populates="skills")
    
