from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import upload, transcribe, diarize, merge


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(transcribe.router)
app.include_router(diarize.router)
app.include_router(merge.router)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.VERSION,
    }
