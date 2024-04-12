# Mockup TTS
# It must be changed with OpenAI TTS
from gtts import gTTS
import base64
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from gtts import gTTS
from io import BytesIO
from fastapi import APIRouter

router = APIRouter()

class InputData(BaseModel):
    data: str

@router.post("/api/handler/text_to_speech/")
async def text_to_speech_endpoint(input_data: InputData):
    """
    Todo:
    openai TTS로 변환
    tts.write_to_fp(buffer)와 비슷한 동작하는 메서드 있는지 확인
    """
    tts = gTTS(text=input_data.data, lang='ko', slow=False)
    buffer = BytesIO()
    tts.write_to_fp(buffer)
    buffer.seek(0)
    
    return StreamingResponse(buffer, media_type="audio/mpeg")