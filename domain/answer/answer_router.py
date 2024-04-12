from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from starlette import status
import io
import json

from database import get_db
from domain.answer import answer_schema, answer_crud
from domain.question import question_crud
from domain.user.user_router import get_current_user
from models import User
from common.agent import stt_llm

router = APIRouter(
    prefix="/api/answer",
)

# answer_content는 임시로 받은 변수, 이후 STT로직이 추가되면 삭제해야함
@router.post("/user_answer_create/{question_id}", response_model=answer_schema.AnswerReponse)
async def user_answer_create(question_id: int, db: Session = Depends(get_db), file: UploadFile = File(...), user = Depends(get_current_user)): # mp3 파일을 인자로 받음
    question = question_crud.get_question(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=404,
                             detail="No unanswered interview question found in the session")
    
    user_voice_answer = io.BytesIO(await file.read())
    user_voice_answer.name = "file.mp3"  # this is the important line

    # STT
    user_text_answer = stt_llm.audio.transcriptions.create(
    model="whisper-1", # 모델 유형 설정
    file=user_voice_answer, # text로 전환할 음성 데이터
    response_format="json" # 응답 타입 설정(json, text, srt, verbose_json, vtt)
    )

    # transcription 객체를 JSON 문자열로 변환
    user_text_answer_json = json.loads(user_text_answer.model_dump_json())
    converted_text = user_text_answer_json['text']
    answer = answer_crud.create_answer(db=db, #db,question 임시값
                              question=question,
                              answer_create=answer_schema.AnswerCreate(content = converted_text)
                              )
    answer_response = answer_schema.AnswerReponse(
         id = answer.id,
         content = answer.content,
         question_id = answer.question_id,
         record_id = answer.question.record.id
    )
    return answer_response


"""
@router.post("/create/{question_id}", response_model=answer_schema.Answer)
def answer_create(question_id: int,
                  _answer_create: answer_schema.AnswerCreate,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):

    # create answer
    question = question_crud.get_question(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found.")
    answer = answer_crud.create_answer(db, question=question,
                              answer_create=_answer_create)
    return answer

@router.post("/create/{question_id}", response_model=answer_schema.Answer)
def answer_create(question_id: int,
                  _answer_create: answer_schema.AnswerCreate,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):

    # create answer
    question = question_crud.get_question(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found.")
    answer = answer_crud.create_answer(db, question=question,
                              answer_create=_answer_create,
                              user=current_user)
    return answer


@router.get("/detail/{answer_id}", response_model=answer_schema.Answer)
def answer_detail(answer_id: int, db: Session = Depends(get_db)):
    answer = answer_crud.get_answer(db, answer_id=answer_id)
    if not answer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found.")
    return answer


@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def answer_update(_answer_update: answer_schema.AnswerUpdate,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_answer = answer_crud.get_answer(db, answer_id=_answer_update.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_answer.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    answer_crud.update_answer(db=db, db_answer=db_answer,
                              answer_update=_answer_update)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def answer_delete(_answer_delete: answer_schema.AnswerDelete,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_answer = answer_crud.get_answer(db, answer_id=_answer_delete.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_answer.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    answer_crud.delete_answer(db=db, db_answer=db_answer)
"""