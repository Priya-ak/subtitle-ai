import pyttsx3

def speak_text(text, lang="en"):
    try:
        engine = pyttsx3.init()

        voices = engine.getProperty('voices')

        # Try different voice indexes if needed
        engine.setProperty('voice', voices[0].id)

        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)

        print("Speaking:", text)  # DEBUG

        engine.say(text)
        engine.runAndWait()

        return {"status": "success"}

    except Exception as e:
        return {"status": "error", "error": str(e)}