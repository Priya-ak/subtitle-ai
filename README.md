<p align="center">
  <h1>🎬 Subtitle AI</h1>
  <h3>✨ Turn Audio & Video into Smart Subtitles with AI</h3>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/AI-Powered-purple?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/FastAPI-Backend-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Streamlit-Frontend-red?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Open%20Source-Love-orange?style=for-the-badge"/>
</p>

<p align="center">
  🎧 Upload → 🧠 Process → 🌍 Translate → 🔊 Speak
</p>

---

## 🌟 What is Subtitle AI?

**Subtitle AI** is a smart AI-powered system that transforms your **audio & video into subtitles**, translates them into different languages, and converts text into speech — all through a clean and simple interface.

💡 Designed to feel like a **Netflix-style subtitle engine** powered by real AI.

---

## 🎥 Live Experience (UI)

- 📂 Clean navigation sidebar  
- 🎧 Upload audio/video  
- 🌍 Select target language  
- 🔤 Text translator  

---

## ⚡ Core Features

### 🎧 Smart Subtitle Generator
- Upload `.mp3`, `.wav`, `.mp4`
- Converts speech → text using AI
- Generates structured subtitles  

---

### 🌍 Multi-Language Translation
- Translate subtitles instantly  
- Supports multiple languages  
- Auto language detection  

---

### 🔊 Text-to-Speech (TTS)
- Convert translated text → audio  
- Download generated speech  

---

### 🧠 Intelligent Processing
- Clean formatting  
- Accurate timestamps  
- Fast response  

---

## 🧱 Tech Stack

| 🚀 Layer       | 💻 Technology        |
|--------------|--------------------|
| Frontend     | Streamlit           |
| Backend      | FastAPI             |
| AI Models    | Whisper / Vosk      |
| Translation  | deep-translator     |
| TTS          | gTTS                |
| Processing   | FFmpeg              |

---

## 📁 Project Structure

<p align="center">
<pre>
subtitle-ai/

├── backend/
│   ├── app/
│   │   ├── utils.py
│   │   ├── tts_utils.py
│   │   ├── srt_utils.py
│   │
│   ├── generated_audio/  🚫 (ignored)
│   ├── models/
│
├── app.py               ⚡ FastAPI Backend
├── requirements.txt
├── .env
├── test_client.py
└── README.md
</pre>
</p>

---

## ⚙️ Setup Guide

### 1️⃣ Clone Repository
```bash
git clone https://github.com/Priya-ak/subtitle-ai.git
cd subtitle-ai
```
### 2️⃣ Install Dependencies
```
pip install -r requirements.txt
```
### 3️⃣ Run Backend
```
uvicorn app:app --reload --port 8000
```

### 4️⃣ Run Frontend
```
streamlit run app.py
```
## 🔌 API Endpoints

| Endpoint       | Purpose              |
|---------------|----------------------|
| `/transcribe` | Generate subtitles   |
| `/translate`  | Translate text       |
| `/tts`        | Text → Speech        |

---

## 🎯 Workflow
Upload File → Speech Recognition → Subtitle Generation → Translation → Audio Output
---

## 🎥 Supported Formats

🎧 Audio: `.mp3`, `.wav`  
🎬 Video: `.mp4`, `.mpeg`  

---

## 🔮 Future Improvements

- ✨ Real-time subtitles  
- 🌐 Multi-language UI  
- 📱 Mobile support  
- 🎙️ Voice cloning  

---

## 👩‍💻 Author

**Priyadharshini**  
🚀 AI Developer  

---

## 💖 Support

- ⭐ Star this repo  
- 🔁 Share it  
- 🤝 Contribute  
