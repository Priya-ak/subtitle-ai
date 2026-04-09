import os, tempfile, requests, wave, json, base64, subprocess
import fasttext
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from app.srt_utils import generate_srt
from dotenv import load_dotenv
import os

load_dotenv()

# OPTIONAL (safe import)
try:
    import whisper
except:
    whisper = None

try:
    from vosk import Model, KaldiRecognizer
except:
    Model = None
    KaldiRecognizer = None

# --- ENV ---
ELEVEN_KEY = os.environ.get("ELEVENLABS_API_KEY")
ELEVEN_VOICE = os.environ.get("ELEVENLABS_VOICE_ID")
VOSK_MODEL_PATH = os.environ.get("VOSK_MODEL_PATH")

# --- LOAD MODELS ONCE ---
FASTTEXT_MODEL = fasttext.load_model("models/fasttext/lid.176.ftz")

tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
translation_model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")

VOSK_MODEL = None

# --- LANGUAGE MAP (IMPORTANT) ---
LANG_MAP = {
    "en": "eng_Latn",
    "hi": "hin_Deva",
    "ta": "tam_Taml",
    "te": "tel_Telu",
    "ml": "mal_Mlym",
    "kn": "kan_Knda",
    "fr": "fra_Latn",
    "es": "spa_Latn",
    "de": "deu_Latn",
    "zh": "zho_Hans",
    "ja": "jpn_Jpan"
}

# --- DETECT LANGUAGE ---
def detect_language(text: str) -> str:
    try:
        text = text.strip().lower()[:500]
        pred = FASTTEXT_MODEL.predict(text)
        lang = pred[0][0].replace("__label__", "")
        return lang
    except:
        return "unknown"

# --- TRANSLATE ---
def translate_text(text: str, src: str, tgt: str) -> str:
    try:
        src = LANG_MAP.get(src, "eng_Latn")
        tgt = LANG_MAP.get(tgt, "eng_Latn")

        tokenizer.src_lang = src
        inputs = tokenizer(text, return_tensors="pt")

        tokens = translation_model.generate(
            **inputs,
            forced_bos_token_id=tokenizer.convert_tokens_to_ids(tgt),
            max_length=256,
            num_beams=2
        )

        return tokenizer.decode(tokens[0], skip_special_tokens=True)

    except Exception as e:
        print("Translation error:", e)
        return text

# --- AUDIO CONVERT ---
def convert_to_wav(path: str) -> str:
    out = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
    subprocess.run(
        ["ffmpeg", "-y", "-i", path, "-ac", "1", "-ar", "16000", out],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return out

# --- TRANSCRIBE ---
def generate_srt(segments):
    def format_time(seconds):
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds - int(seconds)) * 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    srt = ""

    for i, seg in enumerate(segments):
        start = format_time(seg["start"])
        end = format_time(seg["end"])
        text = seg["text"]

        srt += f"{i+1}\n{start} --> {end}\n{text}\n\n"

    return srt
def transcribe_file(path: str, target_language: str = "en") -> dict:
    try:
        wav = convert_to_wav(path)

        text = ""
        segments = []

        # --- WHISPER ---
        if whisper:
            global whisper_model

            if "whisper_model" not in globals():
                whisper_model = whisper.load_model("small")

            result = whisper_model.transcribe(wav, word_timestamps=True)

            text = result.get("text", "").strip()
            segments = result.get("segments", [])

        # --- VOSK FALLBACK ---
        if not text and VOSK_MODEL and KaldiRecognizer:
            wf = wave.open(wav, "rb")
            rec = KaldiRecognizer(VOSK_MODEL, wf.getframerate())

            results = []
            while True:
                data = wf.readframes(4000)
                if not data:
                    break
                if rec.AcceptWaveform(data):
                    res = json.loads(rec.Result())
                    results.append(res.get("text", ""))

            text = " ".join(results).strip()

        # --- CHECK ---
        if not text or len(text) < 3:
            return {"error": "no_speech_detected"}

        # --- LANGUAGE ---
        src = detect_language(text)

        # --- TRANSLATE ---
        # --- TRANSLATE FULL TEXT (keep your logic) ---
        translated = translate_text(text, src, target_language)

        # --- 🔥 NEW: TRANSLATE EACH SEGMENT ---
        translated_segments = []

        for seg in segments:
            original_text = seg.get("text", "")

            try:
                translated_text = translate_text(original_text, src, target_language)
            except:
                translated_text = original_text

            translated_segments.append({
                "start": seg["start"],
                "end": seg["end"],
                "text": original_text,
                "translated": translated_text
            })

        # --- GENERATE SRT (use original segments) ---
        srt = generate_srt(segments)
        return {
            "sourceLanguage": src,
            "transcription": text,
            "translation": translated,   # keep (optional)
            "segments": translated_segments,  # 🔥 important change
            "srt": srt
        }

    except Exception as e:
        return {"error": str(e)}
    
# --- TTS ---
def tts_generate(text: str) -> str:
    if not ELEVEN_KEY or not ELEVEN_VOICE:
        return None

    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVEN_VOICE}"

        headers = {
            "xi-api-key": ELEVEN_KEY,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg"
        }

        payload = {
            "text": text,
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
        }

        r = requests.post(url, headers=headers, json=payload)

        print("STATUS:", r.status_code)
        print("RESPONSE:", r.text)

        if r.status_code == 200:
            import os, uuid

            OUTPUT_DIR = "generated_audio"
            os.makedirs(OUTPUT_DIR, exist_ok=True)

            filename = f"{uuid.uuid4()}.mp3"
            out = os.path.join(OUTPUT_DIR, filename)

            with open(out, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)

            return out, filename

    except Exception as e:
        print("TTS error:", e)

    return None
