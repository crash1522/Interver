from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from fastapi.responses import StreamingResponse
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
from common.agent import stt_llm #tts,stt 공통
from io import BytesIO

router = APIRouter(
    prefix="/api/handler",
)

input_dict: Dict[int, handler_schema.Input] = {}

# DB에 접근하지 않습니다.
# Greeting 이후에 질문을 할 수 있도록 프롬프트 조정 필요
@router.post("/interview_start") #인터뷰 시작 시 new_record.id 생성
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

@router.post("/text_to_speech")
async def text_to_speech(question: question_schema.QuestionCreate):
    
    if not question.content:
        raise HTTPException(status_code=400, detail="No text provided for TTS conversion")
    try:
        # TTS API 호출
        response = stt_llm.audio.speech.create(
            model="tts-1-hd",  # 고화질의 음성 품질 모델 선택
            voice="shimmer",  # 선택된 목소리 유형
            input=question.content,  # 클라이언트로부터 받은 텍스트
            )
        audio_stream = BytesIO(response.content)


        # 클라이언트에게 음성 데이터 전송
        return StreamingResponse(audio_stream, media_type='audio/mpeg')
          
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))