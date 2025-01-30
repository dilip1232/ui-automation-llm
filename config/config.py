import os
from dotenv import load_dotenv

load_dotenv()

EMULATOR_NAME = os.getenv("EMULATOR_NAME")
APK_PATH = os.getenv("APK_PATH")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
llm_config = {
    "config_list": [
        {
            "model": "gemini-pro",
            "api_key": GEMINI_API_KEY,
            "api_type": "google",
            "base_url": "https://generativelanguage.googleapis.com/v1",
        }
    ],
    "temperature": 0.7,
    "max_tokens": 500,
}
