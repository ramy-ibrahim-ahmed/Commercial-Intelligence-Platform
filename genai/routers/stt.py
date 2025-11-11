import os
import tempfile
from fastapi import APIRouter, Request, UploadFile, File, HTTPException

router = APIRouter()


@router.post("/stt")
async def stt(request: Request, file: UploadFile = File(...)):
    nlp = request.app.state.nlp

    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as tmp:
            tmp.write(await file.read())
            speech_path = tmp.name

        text = nlp.speech_to_text("gemini-2.5-flash", speech_path)
        return {"text": text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")

    finally:
        if "speech_path" in locals() and os.path.exists(speech_path):
            os.unlink(speech_path)
