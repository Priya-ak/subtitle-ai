"""
Simple test client to exercise backend endpoints.
Run after starting the FastAPI server (uvicorn app.main:app --reload --port 8000).

This script will:
- POST /api/translate/text
- POST /api/tts
- POST /api/transcribe/voice (if you provide a sample audio file)

Usage:
  python test_client.py

"""
import requests
import base64
import os

BASE = os.environ.get("SUBTITLE_AI_BASE", "http://localhost:8000")


def test_translate():
    payload = {"text": "Hello, how are you?", "targetLanguage": "hi"}
    r = requests.post(f"{BASE}/api/translate/text", json=payload)
    print("translate/text status:", r.status_code)
    print(r.json())


def test_tts():
    payload = {"text": "नमस्ते, आप कैसे हैं?", "language": "hi", "voice": "female", "speed": 1.0}
    r = requests.post(f"{BASE}/api/tts", json=payload)
    print("tts status:", r.status_code)
    data = r.json()
    print("duration:", data.get("duration"))
    b64 = data.get("audioFile")
    if b64:
        out = base64.b64decode(b64)
        open("sample_tts.wav", "wb").write(out)
        print("Wrote sample_tts.wav")


def test_transcribe_file(path="sample.wav"):
    if not os.path.exists(path):
        print("No sample audio found at", path)
        return
    files = {"file": open(path, "rb")}
    r = requests.post(f"{BASE}/api/transcribe/file?targetLanguage=en", files=files)
    print("transcribe/file status:", r.status_code)
    print(r.json())


if __name__ == "__main__":
    test_translate()
    test_tts()
    # optionally test local audio file
    test_transcribe_file("sample.wav")
