from fastapi import APIRouter, HTTPException
from fastapi import Depends
from domain.user.user_router import get_current_user
from domain.handler import handler_schema
from domain.user.user_crud import get_skills
from models import User

from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(
    prefix="/api/input",
)


# DB에 접근하지 않습니다.
@router.post("/create", response_model=handler_schema.Input)
def input_create(db: Session = Depends(get_db), current_user: User = Depends(get_current_user),
                  company_info: handler_schema.CompanyInfo = handler_schema.CompanyInfo(),
                  cover_letter: handler_schema.CoverLetter = handler_schema.CompanyInfo()):
    
    user_info = handler_schema.UserInfo(username = current_user.username,
                                    skills = get_skills(db, current_user.userid),
                                    field = current_user.field)

    _input = handler_schema.Input(user_info = user_info,
                                  company_info = company_info,
                                  cover_letter = cover_letter)
    return _input