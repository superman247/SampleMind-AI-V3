# cli/options/session.py

"""
SampleMindAI – Session Management
Manage session state (e.g., user preferences, project settings).
Future functionality; currently includes a placeholder.
"""

from rich.console import Console
from rich.prompt import Prompt
from utils.config import config
from utils.logger import log_event
import os
import json

console = Console()

class Session:
    """
    A class to manage the session state, including preferences and project settings.
    """
    def __init__(self) -> None:
        self.session_data = {}
        self.session_file = os.path.join(config.CACHE_DIR, "session.json")
        self.load_session()

    def load_session(self) -> None:
        """Load the session data from the session file."""
        if os.path.exists(self.session_file):
            with open(self.session_file, "r") as f:
                self.session_data = json.load(f)
        else:
            console.print(f"[yellow]No existing session data found. Starting a new session.[/yellow]")

    def save_session(self) -> None:
        """Save the session data to the session file."""
        with open(self.session_file, "w") as f:
            json.dump(self.session_data, f, indent=2)

    def update_session(self, key: str, value: str) -> None:
        """Update a session key with a new value."""
        self.session_data[key] = value
        self.save_session()

def main() -> None:
    """
    CLI entrypoint for managing the session.
    """
    console.print("[bold magenta]SampleMindAI – Session Management[/bold magenta]")

    session = Session()

    action = Prompt.ask("What would you like to do?", choices=["1", "2", "3"], default="1")
    
    if action == "1":
        key = Prompt.ask("Enter the session key to update")
        value = Prompt.ask("Enter the new value for this key")
        session.update_session(key, value)
        console.print(f"[green]Session key '{key}' updated to '{value}'[/green]")
        log_event(f"Session key '{key}' updated to '{value}'")

    elif action == "2":
        console.print(f"[cyan]Current session data: {session.session_data}[/cyan]")
        log_event("Session data viewed")

    elif action == "3":
        console.print("[yellow]Exiting without any changes[/yellow]")
        log_event("Exiting session management without changes")

if __name__ == "__main__":
    main()
