from utils.config import config
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def validate():
    if not OPENAI_API_KEY:
        raise ValueError("Missing OPENAI_API_KEY in .env")