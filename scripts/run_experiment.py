# scripts/run_experiment.py
import os
import sys
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# ---------------- PATH FIX ------------------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

DATA_DIR = os.path.join(ROOT_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
# ---------------------------------------------------

from prompts.prompt_variations import generate_prompts

# Load .env file
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

# CHANGE THIS TO TEST DIFFERENT MODELS
MODEL_NAME = "deepseek/deepseek-r1:free"


def sanitize_filename(name: str) -> str:
    """
    Removes characters Windows cannot store in file names.
    """
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    safe = name
    for c in invalid_chars:
        safe = safe.replace(c, "_")
    return safe


def query_model(prompt):
    """
    Sends prompt to OpenRouter and prints raw debug output.
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        resp = requests.post(url, json=payload, headers=headers)
        print("\nRAW API RESPONSE:", resp.text)  # DEBUG PRINT

        if resp.status_code != 200:
            return f"[API Error {resp.status_code}] {resp.text}"

        data = resp.json()

        # Validate structure
        if "choices" not in data or len(data["choices"]) == 0:
            return "[ERROR] Invalid response format"

        content = data["choices"][0]["message"]["content"]
        if not content:
            return "[ERROR] Empty response"

        return content

    except Exception as e:
        return f"[EXCEPTION] {e}"


def run_experiment():
    if not API_KEY:
        print("❌ ERROR: Missing OPENROUTER_API_KEY in .env")
        return

    prompts = generate_prompts()
    results = []

    print(f"\n🔍 Running experiment using model: {MODEL_NAME}\n")

    for p in prompts:
        print(f"→ Sending prompt: {p['hypothesis']} ({p['type']})")

        answer = query_model(p["prompt"])
        print("MODEL RESPONSE:", answer)  # DEBUG PRINT

        results.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "model": MODEL_NAME,
            "hypothesis": p["hypothesis"],
            "type": p["type"],
            "prompt": p["prompt"],
            "response": answer
        })

    # --- FIXED FILE NAME ---
    safe_name = sanitize_filename(MODEL_NAME)
    file_path = os.path.join(DATA_DIR, f"experiment_results_{safe_name}.csv")

    df = pd.DataFrame(results)
    df.to_csv(file_path, index=False, encoding="utf-8")

    print(f"\n✅ Experiment completed successfully!")
    print(f"📁 Saved results to:\n{file_path}\n")


if __name__ == "__main__":
    run_experiment()
