from pydantic import BaseModel
import datetime
from typing import Optional

class Record(BaseModel):
    id: int
    userid: str               
    create_date: datetime.datetime
    rating: Optional[int] = None
    """
    Todo
    nth_round 추가
    """

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class RecordList(BaseModel):
    total: int = 0
    record_list: list[Record] = []

class RecordDelete(BaseModel):
    record_id: int
