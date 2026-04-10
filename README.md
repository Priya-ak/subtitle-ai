# 🎬 Subtitle AI

### 🚀 AI-Powered Subtitles • Translation • Media Intelligence

<p align="center">
  <img src="https://img.shields.io/badge/AI-Subtitle%20Engine-ff416c?style=for-the-badge&logo=ai&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-Frontend-ff4b2b?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-Backend-7c3aed?style=for-the-badge&logo=fastapi&logoColor=white"/>
</p>

---

## 🌟 ✨ Project Overview

**Subtitle AI** is a **next-generation AI tool** designed to convert **audio & video into subtitles**, translate them instantly, and deliver a **cinematic user experience** 🎬

🔥 Built with real-world production concepts
🔥 Designed with Netflix-style UI
🔥 Ready for deployment

---

## 🎯 🚀 Features

### 🎧 Audio / Video Subtitle Generator

✔ Upload MP3 / WAV / MP4
✔ AI Speech Recognition
✔ Real-time subtitle sync
✔ Smooth playback experience

---

### 🌐 Smart Text Translator

✔ Auto language detection
✔ Translate to any language
✔ Fast & accurate output
✔ Clean UI display

---

### 🎬 Netflix-Style Subtitles

✔ Dark cinematic subtitle box
✔ Glow + shadow effects
✔ Real-time sync with media
✔ Premium UI experience

---

### 📥 Export Options

✔ Download `.srt` subtitles
✔ 🎬 Burn subtitles into video (FFmpeg)
✔ Ready-to-share final video

---

## 🖥️ 🎨 UI Experience

✨ Glassmorphism cards
✨ Gradient neon glow
✨ Sidebar navigation (Pro UI)
✨ Smooth buttons & hover effects

👉 Looks like a **real SaaS product**

---

## 🏗️ ⚙️ Tech Stack

| Layer               | Technology     |
| ------------------- | -------------- |
| 🎨 Frontend         | Streamlit      |
| ⚙️ Backend          | FastAPI        |
| 🧠 AI Model         | Whisper / Vosk |
| 🌍 Translation      | Custom API     |
| 🎬 Video Processing | FFmpeg         |

---

## 📁 📦 Project Structure

```
subtitle-ai/
│
├── backend/
│   ├── main.py
│   ├── utils.py
│   ├── srt_utils.py
│   └── requirements.txt
│
├── app.py
├── README.md
└── .gitignore
```

---

## ⚙️ 🔧 Installation

### 🔹 Clone Repository

```bash
git clone https://github.com/Priya-ak/subtitle-ai.git
cd subtitle-ai
```

---

### 🔹 Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 7777
```

---

### 🔹 Frontend Setup

```bash
cd ..
pip install streamlit
streamlit run app.py
```

---

## 🔗 🔥 API Configuration

Before deployment:

```python
API_URL = "http://127.0.0.1:7777/api/subtitles"
```

After deployment:

```python
API_URL = "https://your-backend-url/api/subtitles"
```

---

## 🎬 🚀 Export Video with Subtitles

```bash
ffmpeg -i input.mp4 -vf subtitles=output.srt output.mp4
```

---

## 🌍 🚀 Deployment

### 🎨 Frontend

* Streamlit Cloud
* Render

### ⚙️ Backend

* Render
* Railway
* AWS

---

## 💡 🔮 Future Improvements

🚀 Live subtitle streaming
🌍 Multi-language real-time captions
🎙️ Voice cloning
📱 Mobile app version

---

## 👩‍💻 💼 Author

**Priyadharshini**

🚀 AI Developer
💡 Building real-world AI products

---

## ⭐ 💖 Support

If you like this project:

⭐ Star the repo
📢 Share with others
🚀 Build amazing things

---


