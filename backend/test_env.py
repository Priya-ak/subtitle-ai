import os
from dotenv import load_dotenv

load_dotenv()

print("KEY:", os.getenv("ELEVENLABS_API_KEY"))
print("VOICE:", os.getenv("ELEVENLABS_VOICE_ID"))