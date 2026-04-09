import streamlit as st
import requests
import streamlit.components.v1 as components
import base64
import json
import subprocess
import uuid

API_URL = "http://127.0.0.1:7777/api/subtitles"

st.set_page_config(page_title="Subtitle AI", layout="wide")

# ================= 🎨 FIXED PREMIUM UI =================

st.markdown("""
<style>

/* 🌌 BACKGROUND */
.stApp {
    background: radial-gradient(circle at top, #0f172a, #020617 70%);
    color: #ffffff;
}

/* 🎯 CONTAINER */
.block-container {
    max-width: 1100px;
    margin: auto;
    padding-top: 2rem;
}

/* 🎬 TITLE */
h1 {
    text-align: center;
    font-size: 52px;
    font-weight: 900;
    color: #ffffff;
    text-shadow:
        0 0 10px #ff0055,
        0 0 25px #ff0055,
        0 0 50px #7c3aed;
}

/* 🧾 HERO TEXT */
.hero-text {
    text-align:center;
    font-size:18px;
    color:#cbd5f5;
}

/* 📦 CARD */
.card {
    background: rgba(15, 23, 42, 0.95);
    padding: 22px;
    border-radius: 18px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0px 15px 50px rgba(0,0,0,0.9);
}

/* 🔴 BUTTON */
.stButton>button {
    background: linear-gradient(90deg, #ff0055, #ff4b2b);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 12px 24px;
    font-weight: 700;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px #ff0055;
}

/* 📤 UPLOAD BUTTON FIX */
.stFileUploader button {
    background-color: black !important;
    color: white !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
}

/* Upload text */
.stFileUploader div {
    color: #e2e8f0 !important;
}

/* ✍️ INPUT */
textarea {
    background: #020617 !important;
    color: #ffffff !important;
    border: 1px solid #475569 !important;
}

/* SELECT BOX */
.stSelectbox div {
    background: #020617 !important;
    color: white !important;
}

/* 🌍 LABEL COLORS */
label, .stSelectbox label, .stFileUploader label {
    font-weight: 700 !important;
    font-size: 16px !important;
    color: #38bdf8 !important;  /* bright blue */
}

/* 🎧 SUBTITLE */
.subtitle-box {
    margin-top: 25px;
    font-size: 36px;
    font-weight: 900;
    color: #ffffff;
    text-align: center;
    padding: 16px;
    border-radius: 10px;
    background: rgba(0,0,0,0.85);
    text-shadow:
        2px 2px 10px rgba(0,0,0,1),
        0 0 25px rgba(255,255,255,0.4);
}

/* 🎬 VIDEO */
video {
    box-shadow: 0px 30px 100px rgba(0,0,0,0.9);
    border-radius: 16px;
}

/* 🎧 AUDIO */
audio {
    filter: drop-shadow(0px 10px 30px rgba(0,0,0,0.9));
}

/* 📂 SIDEBAR */
section[data-testid="stSidebar"] {
    background: #020617;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
    font-weight: 600;
}

/* Active menu highlight */
section[data-testid="stSidebar"] .stRadio label {
    color: #38bdf8 !important;
    font-weight: 800;
}

/* Hover effect */
section[data-testid="stSidebar"] label:hover {
    color: #ff4b2b !important;
    transform: translateX(3px);
}

/* Headings */
h2, h3 {
    color: #f472b6 !important;
}

</style>
""",unsafe_allow_html=True)

# ================= HERO =================
st.markdown("""
<div style="text-align:center; margin-bottom:30px;">
    <h1>🎬 Subtitle AI</h1>
    <p class="hero-text">
        AI-powered subtitles • Translation • Media Intelligence
    </p>
</div>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
menu = st.sidebar.radio(
    "📂 Navigation",
    ["🎬 Video / Audio", "🌐 Text Translator"]
)

st.sidebar.markdown("""
<h2 style="color:#ff416c;">🎬 Control Panel</h2>
<p style="color:gray;">Choose your AI feature</p>
""", unsafe_allow_html=True)

# ================= LANGUAGE =================
LANG_OPTIONS = {
    "English": "en",
    "Tamil": "ta",
    "Hindi": "hi",
    "Telugu": "te",
    "Malayalam": "ml",
    "Kannada": "kn",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Chinese": "zh",
    "Japanese": "ja"
}

selected_lang_name = st.selectbox(
    "🌍 Select Target Language",
    list(LANG_OPTIONS.keys()),
    key="lang_select"
)

target_lang = LANG_OPTIONS[selected_lang_name]

# ================= TEXT TRANSLATOR =================
if menu == "🌐 Text Translator":



    st.markdown("## 🌐 Text Translator")

    input_text = st.text_area(
        "✍️ Enter text to translate",
        height=120,
        key="translator_input"
    )

    if st.button("🔁 Translate Text") and input_text.strip():

        with st.spinner("Translating... 🌍"):

            try:
                res = requests.post(
                    "http://127.0.0.1:7777/api/translate/text",
                    params={"text": input_text, "targetLanguage": target_lang}
                )

                result = res.json()

                detected = result.get("sourceLanguage", "")
                translated = result.get("translation", "")

                st.markdown(f"""
                <div class="card" style="text-align:center;">
                    <p>Detected: {detected}</p>
                    <h2>{translated}</h2>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ {e}")

    st.markdown('</div>', unsafe_allow_html=True)

# ================= FUNCTIONS =================
def format_time(seconds):
    return f"{int(seconds//3600):02}:{int((seconds%3600)//60):02}:{int(seconds%60):02},{int((seconds%1)*1000):03}"

def create_srt_from_segments(segments, target_lang):
    srt = ""
    for i, seg in enumerate(segments):
        text = seg.get("translated") if target_lang != "en" else seg.get("text")
        srt += f"{i+1}\n{format_time(seg['start'])} --> {format_time(seg['end'])}\n{text}\n\n"
    return srt

def srt_to_vtt(srt):
    return "WEBVTT\n\n" + srt.replace(",", ".")

# ================= VIDEO / AUDIO =================
if menu == "🎬 Video / Audio":

    

    file = st.file_uploader("Upload Audio / Video", type=["mp3","wav","flac","mp4","mkv"])

    if file:
        st.success("File uploaded successfully ✅")

        if st.button("🚀 Generate Subtitles"):

            res = requests.post(API_URL,
                files={"file": (file.name, file, file.type)},
                data={"targetLanguage": target_lang}
            )

            result = res.json()
            segments = result.get("segments", [])
            srt = create_srt_from_segments(segments, target_lang)

            if file.type.startswith("video"):

                vtt = srt_to_vtt(srt)
                video_b64 = base64.b64encode(file.getvalue()).decode()
                vtt_b64 = base64.b64encode(vtt.encode()).decode()

                components.html(f"""
                <div style="display:flex;justify-content:center;">
                    <video controls autoplay style="max-width:90%;border-radius:16px;">
                        <source src="data:video/mp4;base64,{video_b64}">
                        <track src="data:text/vtt;base64,{vtt_b64}" kind="subtitles" default>
                    </video>
                </div>
                """, height=550)

            else:

                audio_b64 = base64.b64encode(file.getvalue()).decode()
                segments_json = json.dumps(segments)

                components.html(f"""
                <div style="text-align:center;">
                    <audio id="audioPlayer" controls style="width:80%;">
                        <source src="data:audio/mp3;base64,{audio_b64}">
                    </audio>

                    <div id="subtitle" class="subtitle-box"></div>
                </div>

                <script>
                const segments = {segments_json};
                const audio = document.getElementById("audioPlayer");
                const box = document.getElementById("subtitle");

                audio.addEventListener("timeupdate", () => {{
                    let t = audio.currentTime;
                    for (let s of segments) {{
                        if (t >= s.start && t <= s.end) {{
                            box.innerText = "{target_lang}" !== "en"
                                ? (s.translated || s.text)
                                : s.text;
                        }}
                    }}
                }});
                </script>
                """, height=250)

            st.download_button("⬇ Download SRT", srt)

    st.markdown('</div>', unsafe_allow_html=True)