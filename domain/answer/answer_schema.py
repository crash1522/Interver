from pydantic import BaseModel, validator
from typing import Optional

class AnswerCreate(BaseModel):
    content: str

    @validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v


class Answer(BaseModel):
    id: Optional[int] = None
    content: str
    question_id: Optional[int] = None
 
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class AnswerUpdate(AnswerCreate):
    answer_id: int


class AnswerDelete(BaseModel):
    answer_id: int
