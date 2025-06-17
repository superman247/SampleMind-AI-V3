from utils.config import config
# ai_engine/gpt/auto_json_tag.py

from core.ai_backend import query_ai
import os
import json
from rich.console import Console

console = Console()

def auto_json_tag(folder_path, backend="hermes"):
    console.print(f"[bold cyan]AI auto-tagging: Writing tags to JSON for each audio file in {folder_path}[/bold cyan]")
    files = [f for f in os.listdir(folder_path) if f.lower().endswith((".wav", ".mp3", ".flac", ".aiff"))]

    for file in files:
        file_path = os.path.join(folder_path, file)
        prompt = (
            f"Analyze and tag the following audio file: {file_path}. "
            "Respond in JSON format: {\"genre\": ..., \"mood\": ..., \"instrument\": ..., \"bpm\": ...}"
        )
        result = query_ai(prompt, backend=backend)
        try:
            tags = json.loads(result)
        except Exception:
            tags = {"raw": result}
        json_path = file_path + ".json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(tags, f, ensure_ascii=False, indent=2)
        console.print(f"[green]Tagged: {file} → {json_path}[/green]")

def main():
    folder_path = input("Enter folder path containing audio files: ")
    backend = input("Choose AI backend ('hermes' or 'openai') [hermes]: ").strip() or "hermes"
    auto_json_tag(folder_path, backend=backend)

if __name__ == "__main__":
    main()