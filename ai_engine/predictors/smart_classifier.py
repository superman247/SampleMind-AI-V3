from utils.config import config
# ai_engine/predictors/smart_classifier.py

from core.ai_backend import query_ai
import json
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def smart_classify(file_path, backend="hermes"):
    prompt = (
        f"Classify this audio file: {file_path}.\n"
        "Respond in JSON: {\"genre\": ..., \"mood\": ..., \"instrument\": ..., \"bpm\": ..., \"description\": ...}"
    )
    result = query_ai(prompt, backend=backend)
    try:
        tags = json.loads(result)
    except Exception:
        tags = {"raw": result}
    json_path = file_path + ".smartclass.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(tags, f, ensure_ascii=False, indent=2)
    console.print(f"[green]Smart classification saved to: {json_path}[/green]\n[bold yellow]Result:[/bold yellow] {tags}")

def main():
    file_path = Prompt.ask("Enter path to audio file for smart classification")
    backend = Prompt.ask("Choose AI backend ('hermes' for local, 'openai' for cloud)", choices=["hermes", "openai"], default="hermes")
    smart_classify(file_path, backend=backend)

if __name__ == "__main__":
    main()