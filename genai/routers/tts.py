import base64
from pydantic import BaseModel
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import Response

router = APIRouter()


class TTSPayload(BaseModel):
    text: str


@router.post("/tts")
async def tts(request: Request, payload: TTSPayload):
    nlp = request.app.state.nlp

    if not payload.text:
        raise HTTPException(status_code=400, detail="No text provided for TTS.")

    try:
        audio_data = nlp.text_to_speech("gemini-2.5-flash-preview-tts", payload.text)
        audio_bytes = base64.b64decode(audio_data)
        return Response(content=audio_bytes, media_type="audio/mp3")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating audio: {str(e)}")
