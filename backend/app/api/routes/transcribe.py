from fastapi import APIRouter, HTTPException
from app.services.audio.transcriber import transcribe

router = APIRouter(prefix="/transcribe", tags=["Transcription"])


@router.post("/{job_id}")
def transcribe_meeting(job_id: str):
    try:
        result = transcribe(job_id)
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")