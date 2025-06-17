from utils.config import config
# cli/options/manual_tag.py

from core.ai_backend import query_ai
import os
import json
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def manual_tag(file_path):
    tags = {}
    for field in ["genre", "mood", "instrument", "bpm"]:
        tags[field] = Prompt.ask(f"Enter {field} (or leave blank for AI suggest)")

    # If any field is blank, suggest from AI
    if any(v.strip() == "" for v in tags.values()):
        use_ai = Prompt.ask("One or more fields are blank. Suggest tags with AI? (y/n)", choices=["y", "n"], default="y")
        if use_ai == "y":
            backend = Prompt.ask("Choose AI backend ('hermes' or 'openai')", choices=["hermes", "openai"], default="hermes")
            prompt = (
                f"Suggest complete tags (genre, mood, instrument, bpm) for this audio file: {file_path}. "
                f"Respond in JSON. If you already have tags, consider them: {json.dumps(tags)}"
            )
            result = query_ai(prompt, backend=backend)
            try:
                ai_tags = json.loads(result)
            except Exception:
                ai_tags = {"raw": result}
            # Only fill blanks
            for k in tags:
                if tags[k].strip() == "" and k in ai_tags:
                    tags[k] = ai_tags[k]
    # Write tags to JSON
    json_path = file_path + ".json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(tags, f, ensure_ascii=False, indent=2)
    console.print(f"[green]Manual (and AI-assisted) tags written to: {json_path}[/green]")

def main():
    file_path = Prompt.ask("Enter path to audio file")
    manual_tag(file_path)

if __name__ == "__main__":
    main()