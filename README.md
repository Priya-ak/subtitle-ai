# Subtitle AI

Minimal scaffold for Subtitle AI — an offline-capable subtitle, translation, and TTS app.

Quickstart

- Backend (FastAPI):

  ```bash
  cd backend
  python -m venv .venv
  .venv\Scripts\activate    # Windows
  pip install -r requirements.txt
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
  ```

- Frontend (Vite + React + Tailwind):

  ```bash
  cd frontend
  npm install
  npm run dev
  ```

Notes
- Backend contains API endpoint stubs and model integration hooks in `backend/app`.
- Frontend is a lightweight three-panel UI scaffold in `frontend/src`.
- This repo intentionally provides local hooks for Whisper, MarianMT and Coqui TTS — you will need to download models locally to run fully offline.

API Endpoints (scaffolded)

- `POST /api/transcribe/voice` — voice file upload -> transcription, translation, subtitles
- `POST /api/translate/text` — text translation
- `POST /api/transcribe/file` — file upload -> subtitles + SRT (base64)
- `POST /api/tts` — text-to-speech -> base64 audio
- `POST /api/detect` — language detection
- `POST /api/speaker` — speaker diarization

Testing endpoints (curl)

- Translate text:

```bash
curl -X POST "http://localhost:8000/api/translate/text" -H "Content-Type: application/json" -d '{"text":"Hello, how are you?","targetLanguage":"hi"}'
```

- TTS:

```bash
curl -X POST "http://localhost:8000/api/tts" -H "Content-Type: application/json" -d '{"text":"नमस्ते","language":"hi","voice":"female"}'
```

- Upload audio file (multipart form):

```bash
curl -X POST "http://localhost:8000/api/transcribe/file?targetLanguage=en" -F "file=@/path/to/audio.mp3"
```

You can also use `backend/test_client.py` to run quick checks (requires `requests`).

Docker / Electron (offline packaging)

- Docker Compose (build backend + frontend):

```bash
docker-compose build
docker-compose up
```

Place model folders under `backend/models` and set `VOSK_MODEL_PATH` accordingly (docker-compose mounts `./backend/models` to `/app/models`).

- Electron (desktop wrapper, dev):

```bash
cd electron
npm install
npm start
```

This will spawn a local backend (via `uvicorn`) and open the frontend at `http://localhost:5173`. For a production build, build the frontend and point Electron to the static files.
