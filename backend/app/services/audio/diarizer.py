from pyannote.audio import Pipeline
from pathlib import Path
from app.core.config import settings
import torch

print("[Diarizer] Loading speaker diarization model...")
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    token=settings.HF_TOKEN
)
print("[Diarizer] Model ready.")


def find_uploaded_file(job_id: str) -> Path:
    upload_dir = Path(settings.UPLOAD_DIR)
    for file in upload_dir.iterdir():
        if file.stem == job_id:
            return file
    raise FileNotFoundError(f"No file found for job_id: {job_id}")


def diarize(job_id: str) -> dict:
    audio_path = find_uploaded_file(job_id)

    print(f"[Diarizer] Processing: {audio_path}")
    diarization = pipeline(str(audio_path))

    print(f"[Diarizer] Output type: {type(diarization)}")

    segments = []

    # New pyannote API — use speaker_diarization annotation directly
    annotation = diarization.speaker_diarization
    for segment, _, speaker in annotation.itertracks(yield_label=True):
        segments.append({
            "start":   round(segment.start, 2),
            "end":     round(segment.end, 2),
            "speaker": speaker,
        })

    return {
        "job_id": job_id,
        "segments": segments,
        "num_speakers": len(set(s["speaker"] for s in segments)),
    }