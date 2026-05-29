import uuid
import aiofiles
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.config import settings

router = APIRouter(prefix="/upload", tags=["Upload"])

ALLOWED_EXTENSIONS = {".mp3", ".mp4", ".wav", ".m4a", ".webm"}
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500 MB


@router.post("/")
async def upload_meeting(file: UploadFile = File(...)):

    # Validate extension
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: {ALLOWED_EXTENSIONS}"
        )

    # Generate unique job ID
    job_id = str(uuid.uuid4())

    # Build save path — uploads/<job_id>.<ext>
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    save_path = upload_dir / f"{job_id}{ext}"

    # Stream file to disk
    size = 0
    async with aiofiles.open(save_path, "wb") as out:
        while chunk := await file.read(1024 * 1024):  # 1MB chunks
            size += len(chunk)
            if size > MAX_FILE_SIZE:
                save_path.unlink(missing_ok=True)  # delete partial file
                raise HTTPException(status_code=413, detail="File too large (max 500MB)")
            await out.write(chunk)

    return {
        "job_id": job_id,
        "filename": file.filename,
        "saved_as": str(save_path),
        "size_mb": round(size / (1024 * 1024), 2),
        "status": "uploaded"
    }