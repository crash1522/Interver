from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Dict 

from domain.user import user_schema, user_router
from common.handler import handler_schema
from domain.user import user_crud, user_schema
from domain.record import record_crud
from domain.question import question_schema
from common import agent
from common.agent import agent_dict
from database import get_db

router = APIRouter(
    prefix="/api/handler",
)

input_dict: Dict[int, handler_schema.Input] = {}
q_cnt_dict: Dict[int, question_schema.QuestionCount] = {}

# DB에 접근하지 않습니다.
# Greeting 이후에 질문을 할 수 있도록 프롬프트 조정 필요
@router.post("/interview_start")
async def interview_start(
                    db: Session = Depends(get_db),
                    user: user_schema.User = Depends(user_router.get_current_user),
                    company_info: handler_schema.CompanyInfo = handler_schema.CompanyInfo(),
                    cover_letter: handler_schema.CoverLetter = handler_schema.CoverLetter(),
                    q_num: int = 10,):
    global agent_dict, q_cnt_dict
    user_info = handler_schema.UserInfo(username = user.username,
                                    skills = user_crud.get_skills(db, user.userid),
                                    field = user.field,
                                    q_num = q_num)

    new_input = handler_schema.Input(user_info = user_info,
                                  company_info = company_info,
                                  cover_letter = cover_letter)
    # input_dict[current_user.id] = new_input
    new_record = record_crud.create_record(db, user)
    if not new_record:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                       detail="record를 생성하는데 실패했습니다.")
        # 새로운 agent 생성 후, 메모리에 저장

    new_agent = agent.create_agent(new_input)
    if not new_agent:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                       detail="agent를 생성하는데 실패했습니다.")
    agent_dict[new_record.id] = new_agent
    q_cnt_dict[new_record.id] = question_schema.QuestionCount(
        required_question_num = q_num,
        cur_question_num = 0
    )
    return new_record.id