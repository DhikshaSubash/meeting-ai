from fastapi import APIRouter, HTTPException
from app.services.audio.diarizer import diarize

router = APIRouter(prefix="/diarize", tags=["Diarization"])


@router.post("/{job_id}")
def diarize_meeting(job_id: str):
    try:
        result = diarize(job_id)
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Diarization failed: {str(e)}")