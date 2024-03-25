from pydantic import BaseModel
import datetime
from models import Question

class Record(BaseModel):
    id: int
    userid: str               
    create_date: datetime.datetime
    questions: list[Question] = []