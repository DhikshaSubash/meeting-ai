import whisper
import torch
from pathlib import Path
from app.core.config import settings

# Load model once at startup — not on every request
# Options: "tiny", "base", "small", "medium", "large"
# Start with "base" — good balance of speed and accuracy
MODEL_SIZE = "base"

print(f"[Whisper] Loading model: {MODEL_SIZE}")
model = whisper.load_model(MODEL_SIZE)
print(f"[Whisper] Model ready. Using: {'GPU' if torch.cuda.is_available() else 'CPU'}")


def find_uploaded_file(job_id: str) -> Path:
    """Find the uploaded file by job_id regardless of extension."""
    upload_dir = Path(settings.UPLOAD_DIR)
    for file in upload_dir.iterdir():
        if file.stem == job_id:
            return file
    raise FileNotFoundError(f"No file found for job_id: {job_id}")


def transcribe(job_id: str) -> dict:
    """
    Run Whisper on the uploaded file and return structured transcript.
    """
    audio_path = find_uploaded_file(job_id)

    print(f"[Whisper] Transcribing: {audio_path}")

    result = model.transcribe(
        str(audio_path),
        verbose=False,
        word_timestamps=False,
    )

    # Build structured segments
    segments = []
    for seg in result["segments"]:
        segments.append({
            "start": round(seg["start"], 2),
            "end": round(seg["end"], 2),
            "text": seg["text"].strip(),
        })

    return {
        "job_id": job_id,
        "language": result.get("language", "en"),
        "full_text": result["text"].strip(),
        "segments": segments,
    }