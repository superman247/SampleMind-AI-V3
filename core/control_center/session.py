from utils.config import config
# core/control_center/session.py

import json
from pathlib import Path
from typing import Any, Dict
from datetime import datetime
from utils.logger import log_event  # Adjusted import path to match project structure

# Path to session file
SESSION_FILE = Path("data/session/session_state.json")

class SessionManager:
    """
    Manages CLI session state for SampleMind.
    Includes saving, loading, updating, and clearing persistent state across CLI usage.
    """

    def __init__(self):
        """Initialize session with default empty state and timestamp."""
        self.state: Dict[str, Any] = {}
        self.timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def load_session(self) -> None:
        """
        Load session state from the session file.
        Logs an error if the session file cannot be loaded.
        """
        try:
            if SESSION_FILE.exists():
                with open(SESSION_FILE, 'r') as file:
                    self.state = json.load(file)
                log_event(f"[INFO] Session loaded successfully at {self.timestamp}.")
            else:
                log_event(f"[WARNING] No existing session file found at {self.timestamp}.")
        except json.JSONDecodeError as e:
            log_event(f"[ERROR] JSON decoding error while loading session: {str(e)}")
        except Exception as e:
            log_event(f"[ERROR] Error loading session: {str(e)}")

    def save_session(self) -> None:
        """
        Save the current session state to the session file.
        """
        try:
            with open(SESSION_FILE, 'w') as file:
                json.dump(self.state, file, indent=4)
            log_event(f"[INFO] Session saved successfully at {self.timestamp}.")
        except Exception as e:
            log_event(f"[ERROR] Error saving session: {str(e)}")

    def update_session(self, key: str, value: Any) -> None:
        """
        Update session state with a new key-value pair.
        """
        self.state[key] = value
        log_event(f"[INFO] Session updated with key: {key} at {self.timestamp}.")

    def clear_session(self) -> None:
        """
        Clear the current session state.
        """
        self.state.clear()
        log_event(f"[INFO] Session cleared at {self.timestamp}.")

    def get_session_state(self) -> Dict[str, Any]:
        """
        Get the current session state.
        """
        return self.state