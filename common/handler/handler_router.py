from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Dict 

from domain.user import user_schema, user_router
from common.handler import handler_schema
from domain.user import user_crud, user_schema
from domain.record import record_crud
from common import agent
from common.agent import agent_dict
from database import get_db

router = APIRouter(
    prefix="/api/handler",
)

input_dict: Dict[int, handler_schema.Input] = {}

# DB에 접근하지 않습니다.
# Greeting 이후에 질문을 할 수 있도록 프롬프트 조정 필요
@router.post("/interview_start")
async def interview_start(user: user_schema.User,
                  db: Session = Depends(get_db),
                  company_info: handler_schema.CompanyInfo = handler_schema.CompanyInfo(),
                  cover_letter: handler_schema.CoverLetter = handler_schema.CompanyInfo(),
                   current_user: user_schema.User = Depends(user_router.get_current_user),):
    
    user_info = handler_schema.UserInfo(username = user.username,
                                    skills = user_crud.get_skills(db, user.userid),
                                    field = user.field)

    new_input = handler_schema.Input(user_info = user_info,
                                  company_info = company_info,
                                  cover_letter = cover_letter)
    input_dict[current_user.id] = new_input
    new_record = record_crud.create_record(db, current_user)
    if not new_record:
        HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                       detail="record를 생성하는데 실패했습니다.")
        # 새로운 agent 생성 후, 메모리에 저장
    new_agent = agent.create_agent(new_input)
    agent_dict[new_record.id] = new_agent

    return new_record.id