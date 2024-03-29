from pydantic import BaseModel
import datetime

class Record(BaseModel):
    id: int
    userid: str               
    create_date: datetime.datetime
    rating: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class RecordList(BaseModel):
    total: int = 0
    record_list: list[Record] = []

class RecordDelete(BaseModel):
    record_id: int
