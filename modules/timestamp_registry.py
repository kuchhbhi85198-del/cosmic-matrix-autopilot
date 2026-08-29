import json
import sys
from pathlib import Path
from typing import Dict, Any, List

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs"
REGISTRY_FILE = LOGS_DIR / "permanent_timestamp_registry.json"

LOGS_DIR.mkdir(parents=True, exist_ok=True)


class TimestampRegistry:
    """
    Permanent Immutable Timestamp & Scene Registry:
    Guarantees that once a timestamp range is sliced from a video,
    that EXACT video and timestamp range (or overlapping seconds) can NEVER be cut again!
    """
    def __init__(self):
        self.registry = self._load()

    def _load(self) -> List[Dict[str, Any]]:
        if REGISTRY_FILE.exists():
            try:
                with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data if isinstance(data, list) else []
            except Exception:
                return []
        return []

    def _save(self):
        with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.registry, f, indent=2)

    def is_timestamp_used(self, video_id: str, start_sec: int, duration_sec: int = 35) -> bool:
        """
        Checks if the requested time range [start, start + duration] overlaps
        with ANY previously sliced moment from this video.
        """
        end_sec = start_sec + duration_sec
        for record in self.registry:
            if record.get("video_id") == video_id:
                r_start = record.get("start_sec", 0)
                r_end = record.get("end_sec", r_start + record.get("duration_sec", 35))
                # Check for overlap: max(start1, start2) < min(end1, end2)
                if max(start_sec, r_start) < min(end_sec, r_end):
                    return True
        return False

    def mark_used(self, video_id: str, start_sec: int, duration_sec: int, hook: str = "", yt_url: str = ""):
        """
        Permanently registers a sliced timestamp range.
        """
        record = {
            "video_id": video_id,
            "start_sec": start_sec,
            "end_sec": start_sec + duration_sec,
            "duration_sec": duration_sec,
            "hook": hook,
            "yt_url": yt_url
        }
        self.registry.append(record)
        self._save()
        print(f"[*] 🔒 [PERMANENT LOCK] Video '{video_id}' at [{start_sec}s - {start_sec + duration_sec}s] locked forever!")


# Global singleton instance
timestamp_registry = TimestampRegistry()
