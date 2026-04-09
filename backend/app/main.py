import os, tempfile, base64
from fastapi import FastAPI, UploadFile, File, Form
from app.utils import detect_language, translate_text, transcribe_file, tts_generate
from app.utils import tts_generate 
from deep_translator import GoogleTranslator
from fastapi.staticfiles import StaticFiles
from fastapi import UploadFile, File, Form
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Subtitle AI -- Backend")
app.mount("/audio", StaticFiles(directory="generated_audio"), name="audio")

# --- Language Detection ---
@app.post("/api/detect")
async def detect(text: str):
    try:
        lang = detect_language(text)
        return {"detectedLanguage": lang}
    except Exception as e:
        return {"error": "detection_failed", "message": str(e)}

# --- Text Translation ---
@app.post("/api/translate/text")
async def translate(text: str, targetLanguage: str):
    try:
        src = detect_language(text)
        translation = translate_text(text, src, targetLanguage)
        return {
            "sourceLanguage": src,
            "translation": translation,
            "subtitles": [{"timestamp": None, "text": translation}]
        }
    except Exception as e:
        return {"error": "translation_failed", "message": str(e)}

# --- File Transcription ---
@app.post("/api/transcribe/file")
async def transcribe_file_endpoint(file: UploadFile = File(...), targetLanguage: str = Form("en")):
    try:
        suffix = os.path.splitext(file.filename)[1]
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        content = await file.read()
        tmp.write(content)
        tmp.close()

        result = transcribe_file(tmp.name, targetLanguage)

        try:
            os.remove(tmp.name)
        except Exception:
            pass

        return result
    except Exception as e:
        return {"error": "transcribe_file_failed", "message": str(e)}

# --- Text-to-Speech ---
@app.post("/api/tts")
def tts(text: str):
    result = tts_generate(text)

    if not result:
        return {"error": "TTS failed"}

    audio_path, filename = result

    return {
        "audio_url": f"http://127.0.0.1:7777/audio/{filename}"
    }
@app.post("/api/subtitles")
async def subtitles(file: UploadFile = File(...), targetLanguage: str = Form("en")):

    import tempfile

    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(await file.read())
    temp.close()

    result = transcribe_file(temp.name, targetLanguage)

    return result