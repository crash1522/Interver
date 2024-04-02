from fastapi import APIRouter, HTTPException
from fastapi import Depends
from domain.user.user_router import get_current_user
from common.handler import handler_schema
from domain.user import user_crud, user_schema
from models import User

from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(
    prefix="/api/input",
)


# DB에 접근하지 않습니다.
@router.post("/create", response_model=handler_schema.Input)
def input_create(user: user_schema.User,
                  db: Session = Depends(get_db),
                  company_info: handler_schema.CompanyInfo = handler_schema.CompanyInfo(),
                  cover_letter: handler_schema.CoverLetter = handler_schema.CompanyInfo(),):
    
    user_info = handler_schema.UserInfo(username = user.username,
                                    skills = user_crud.get_skills(db, user.userid),
                                    field = user.field)

    _input = handler_schema.Input(user_info = user_info,
                                  company_info = company_info,
                                  cover_letter = cover_letter)
    return _input