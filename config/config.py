import os
from dotenv import load_dotenv

load_dotenv()
EMULATOR_NAME = os.getenv("EMULATOR_NAME", "emulator-5554")
APK_PATH = os.getenv("APK_PATH")
APP_PACKAGE = os.getenv("APP_PACKAGE")
APP_ACTIVITY = os.getenv("APP_ACTIVITY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# LLM configuration for autogen using OpenAI
llm_config = {
    "config_list": [
        {
            "model": "gpt-4",
            "api_key": OPENAI_API_KEY,
            "api_type": "openai",
            "base_url": "https://api.openai.com/v1",
        }
    ],
    "temperature": 0.7,
    "max_tokens": 500,
}
