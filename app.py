import streamlit as st
import requests
import streamlit.components.v1 as components
import base64
import json

API_URL = "http://127.0.0.1:7777/api/subtitles"

st.set_page_config(page_title="Subtitle AI", layout="wide")

# ================= 🎨 WHITE UI =================
st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background: #f8fafc;
    color: #1e293b;
}

/* TITLE */
h1 {
    text-align: center;
    font-size: 48px;
    font-weight: 900;
    color: #1e293b;
}

/* HERO TEXT */
.hero-text {
    text-align:center;
    font-size:18px;
    color:#475569;
}

/* CARD */
.card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    margin-bottom: 20px;
    border: 1px solid #e2e8f0;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.08);
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 12px 24px;
    font-weight: 700;
}

.stButton>button:hover {
    transform: scale(1.05);
}

/* FILE UPLOAD */
.stFileUploader {
    border: 2px dashed #cbd5f5;
    padding: 15px;
    border-radius: 12px;
    background: white;
}

/* LABEL */
label {
    color: #2563eb !important;
    font-weight: 700;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #ffffff;
}
section[data-testid="stSidebar"] * {
    color: #1e293b !important;
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
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

# ================= LANG =================
LANG_OPTIONS = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml",
}

st.markdown("### 🌍 Select Target Language")

selected_lang_name = st.selectbox(
    "",
    list(LANG_OPTIONS.keys())
)

target_lang = LANG_OPTIONS[selected_lang_name]

# ================= FUNCTIONS =================
def format_time(seconds):
    return f"{int(seconds//3600):02}:{int((seconds%3600)//60):02}:{int(seconds%60):02},{int((seconds%1)*1000):03}"

def create_srt(segments):
    srt = ""
    for i, seg in enumerate(segments):
        text = seg.get("translated") or seg.get("text")
        srt += f"{i+1}\n{format_time(seg['start'])} --> {format_time(seg['end'])}\n{text}\n\n"
    return srt

# ================= TEXT =================
if menu == "🌐 Text Translator":

    text = st.text_area("Enter text")

    if st.button("Translate"):
        res = requests.post(
            "http://127.0.0.1:7777/api/translate/text",
            params={"text": text, "targetLanguage": target_lang}
        )
        data = res.json()

        st.markdown(f"""
        <div class="card">
            <p><b>Detected Language:</b> {data.get("sourceLanguage")}</p>
            <h2>{data.get("translation")}</h2>
        </div>
        """, unsafe_allow_html=True)

# ================= VIDEO / AUDIO =================
if menu == "🎬 Video / Audio":

    file = st.file_uploader("Upload Audio / Video", type=["mp3","wav","mp4"])

    if file:
        st.success("Uploaded successfully ✅")

        if st.button("🚀 Generate Subtitles"):

            res = requests.post(API_URL,
                files={"file": (file.name, file, file.type)},
                data={"targetLanguage": target_lang}
            )

            data = res.json()
            segments = data.get("segments", [])

            srt = create_srt(segments)

            # ================= VIDEO =================
            if file.type.startswith("video"):

                video_b64 = base64.b64encode(file.getvalue()).decode()
                segments_json = json.dumps(segments)

                components.html(f"""
                <div style="position:relative; text-align:center;">

                <video id="video" controls style="max-width:90%; border-radius:12px;">
                    <source src="data:video/mp4;base64,{video_b64}">
                </video>

                <div id="subtitle"
                style="
                position:absolute;
                bottom:6%;
                left:50%;
                transform:translateX(-50%);
                width:auto;
                max-width:80%;

                text-align:center;
                font-size:22px;
                font-weight:600;
                color:white;
                line-height:1.4;

                padding:6px 12px;
                background:rgba(0,0,0,0.4);
                border-radius:6px;

                text-shadow: 2px 2px 6px rgba(0,0,0,0.9);
                ">
                </div>

                <script>
                const segments = {segments_json};
                const video = document.getElementById("video");
                const box = document.getElementById("subtitle");

                video.addEventListener("timeupdate", () => {{
                    let t = video.currentTime;

                    for (let s of segments) {{
                        if (t >= s.start && t <= s.end) {{

                            let text = "{target_lang}" !== "en"
                                ? (s.translated || s.text)
                                : s.text;


                            box.innerText = s.translated || s.text;
                        }}
                    }}
                }});
                </script>
                """, height=520)

            # ================= AUDIO =================
            else:

                audio_b64 = base64.b64encode(file.getvalue()).decode()
                segments_json = json.dumps(segments)

                components.html(f"""
                <div style="text-align:center">

                <audio id="audio" controls style="width:80%">
                    <source src="data:audio/mp3;base64,{audio_b64}">
                </audio>

                <div id="subtitle"
                style="
                margin-top:20px;
                font-size:28px;
                font-weight:800;
                color:#1e293b;
                ">
                </div>

                </div>

                <script>
                const segments = {segments_json};
                const audio = document.getElementById("audio");
                const box = document.getElementById("subtitle");

                audio.addEventListener("timeupdate", () => {{
                    let t = audio.currentTime;

                    for (let s of segments) {{
                        if (t >= s.start && t <= s.end) {{

                            let text = "{target_lang}" !== "en"
                                ? (s.translated || s.text)
                                : s.text;

                            box.innerText = text;
                        }}
                    }}
                }});
                </script>
                """, height=300)

            st.download_button("⬇ Download SRT", srt)