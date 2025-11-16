# scripts/setup_environment.py
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def verify_openrouter_connection():
    """
    Verifies connection to OpenRouter API using API key from .env
    """
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        print(" ERROR: OPENROUTER_API_KEY not found in .env")
        return

    url = "https://openrouter.ai/api/v1/models"
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        resp = requests.get(url, headers=headers)

        if resp.status_code == 200:
            print(" OpenRouter connection successful!")
        else:
            print(" Failed:", resp.text)
    except Exception as e:
        print(" Error:", e)


if __name__ == "__main__":
    verify_openrouter_connection()
