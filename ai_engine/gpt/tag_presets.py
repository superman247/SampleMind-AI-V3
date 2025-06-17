from utils.config import config
# ai_engine/gpt/tag_presets.py

from core.ai_backend import query_ai
from rich.console import Console
from rich.prompt import Prompt
import json

console = Console()

PRESET_PROMPTS = {
    "techno": "Suggest ideal genre, mood, instrument, and bpm tags for a classic techno drum loop.",
    "lofi": "Suggest genre, mood, instrument, and bpm tags for a typical lo-fi hiphop sample.",
    "trap": "Suggest tags for a modern trap beat (genre, mood, instrument, bpm)."
}

def get_preset_tags(preset, backend="hermes"):
    if preset not in PRESET_PROMPTS:
        console.print(f"[red]Unknown preset: {preset}[/red]")
        return
    prompt = PRESET_PROMPTS[preset]
    result = query_ai(prompt, backend=backend)
    try:
        tags = json.loads(result)
    except Exception:
        tags = {"raw": result}
    console.print(f"[bold green]Preset tags for '{preset}':[/bold green] {tags}")

def main():
    console.print("[bold cyan]AI Tag Preset Generator[/bold cyan]")
    preset = Prompt.ask("Choose preset", choices=list(PRESET_PROMPTS.keys()))
    backend = Prompt.ask("Choose AI backend ('hermes' or 'openai')", choices=["hermes", "openai"], default="hermes")
    get_preset_tags(preset, backend=backend)

if __name__ == "__main__":
    main()