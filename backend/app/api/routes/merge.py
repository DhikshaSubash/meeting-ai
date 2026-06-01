from fastapi import APIRouter, HTTPException
from app.services.audio.transcriber import transcribe
from app.services.audio.diarizer import diarize
from app.services.audio.merger import (
    merge_transcript_with_speakers,
    clean_text,
    build_readable_transcript
)

router = APIRouter(prefix="/merge", tags=["Merge"])


@router.post("/{job_id}")
def merge_meeting(job_id: str):
    """
    Full pipeline: transcribe + diarize + merge into labeled transcript.
    """
    try:
        # Step 1 — Transcribe
        print(f"[Merge] Transcribing {job_id}...")
        transcript = transcribe(job_id)

        # Step 2 — Diarize
        print(f"[Merge] Diarizing {job_id}...")
        diarization = diarize(job_id)

        # Step 3 — Clean each whisper segment
        cleaned_segments = []
        for seg in transcript["segments"]:
            cleaned_segments.append({
                **seg,
                "text": clean_text(seg["text"])
            })

        # Step 4 — Merge
        merged = merge_transcript_with_speakers(
            whisper_segments=cleaned_segments,
            diarization_segments=diarization["segments"]
        )

        # Step 5 — Build readable transcript
        readable = build_readable_transcript(merged)

        return {
            "job_id":        job_id,
            "num_speakers":  diarization["num_speakers"],
            "language":      transcript["language"],
            "segments":      merged,
            "full_text":     transcript["full_text"],
            "readable":      readable,
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Merge failed: {str(e)}")