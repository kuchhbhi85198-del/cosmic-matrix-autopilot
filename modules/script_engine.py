import sys
import json
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN_JSON = BASE_DIR / "assets" / "cleaned_726_science_scripts.json"
HISTORY_FILE = BASE_DIR / "logs" / "used_scripts_history.json"

class CosmicScriptEngine:
    def __init__(self):
        if CLEAN_JSON.exists():
            with open(CLEAN_JSON, "r", encoding="utf-8") as f:
                self.scripts = json.load(f)
        else:
            self.scripts = []
        self.used_ids = self._load_history()

    def _load_history(self) -> list:
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def _save_history(self, item_id: int):
        self.used_ids.append(item_id)
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.used_ids, f, indent=2)

    def get_next_pro_script(self) -> dict:
        """
        Picks the next 100% pure science script from the 543 cleaned database.
        Zero conversational chatter, zero AI greetings, zero names.
        """
        available = [s for s in self.scripts if s["id"] not in self.used_ids]
        if not available:
            self.used_ids = []
            available = self.scripts

        chosen = available[0] # Take sequentially
        self._save_history(chosen["id"])

        return {
            "source_file": chosen.get("source_file", f"Science_Script_{chosen['id']}"),
            "narration": chosen["narration"],
            "top_hook": chosen["headline"],
            "topic_tag": chosen["tag"]
        }

if __name__ == "__main__":
    engine = CosmicScriptEngine()
    data = engine.get_next_pro_script()
    print("Top Hook:", data["top_hook"])
    print("Topic Tag:", data["topic_tag"])
    print("Narration:", data["narration"])
