# Meeting AI

An intelligent meeting analysis system that transcribes, diarizes, summarizes, and extracts action items from meeting recordings.

## Tech Stack
- **Backend**: Python 3.11 + FastAPI + PostgreSQL
- **AI/NLP**: Whisper, pyannote.audio, HuggingFace Transformers, spaCy, BERTopic, FAISS
- **Frontend**: React + Vite

## Quickstart
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Project Structure
meeting-ai/
├── backend/          # FastAPI + all NLP services
├── frontend/         # React dashboard
├── uploads/          # Uploaded audio/video (gitignored)
├── models/           # Downloaded AI models (gitignored)
├── docker/           # Dockerfiles
└── .github/          # CI/CD workflows
