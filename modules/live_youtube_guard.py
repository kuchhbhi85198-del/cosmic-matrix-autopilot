import sys
import pickle
from datetime import datetime, timezone, timedelta
from pathlib import Path
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

IST = timezone(timedelta(hours=5, minutes=30))

def get_ist_now() -> datetime:
    return datetime.now(timezone.utc).astimezone(IST)

def has_channel_posted_in_slot(token_path: Path, slot_type: str) -> bool:
    """
    Direct Live YouTube API Check:
    Queries the actual YouTube Channel directly to see if any video was already
    published in the specified slot window today.
    Zero dependency on local files or git logs!
    """
    if not token_path.exists():
        print(f"[!] Warning: Token file {token_path} not found for live channel check.")
        return False

    try:
        with open(token_path, "rb") as f:
            creds = pickle.load(f)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        
        yt = build("youtube", "v3", credentials=creds)
        res = yt.search().list(
            part="snippet",
            forMine=True,
            type="video",
            order="date",
            maxResults=10
        ).execute()

        ist_now = get_ist_now()
        today_date = ist_now.date()
        current_hour = ist_now.hour

        # Determine slot start and end hours in IST
        if slot_type == "morning":
            slot_start_h, slot_end_h = 4, 12
        elif slot_type == "afternoon":
            slot_start_h, slot_end_h = 12, 17
        elif slot_type == "evening":
            slot_start_h, slot_end_h = 17, 19
        elif slot_type == "night":
            slot_start_h, slot_end_h = 19, 24
        else:
            slot_start_h, slot_end_h = 0, 24

        for item in res.get("items", []):
            pub_raw = item["snippet"].get("publishedAt")
            if not pub_raw:
                continue
            pub_utc = datetime.fromisoformat(pub_raw.replace("Z", "+00:00"))
            pub_ist = pub_utc.astimezone(IST)

            # If video was published TODAY in this exact slot window
            if pub_ist.date() == today_date and slot_start_h <= pub_ist.hour < slot_end_h:
                title = item["snippet"].get("title", "")
                vid = item["id"].get("videoId", "")
                print(f"🛑 [LIVE YOUTUBE GUARD] Found video already live on channel for today's {slot_type.upper()} slot!")
                print(f"   -> Live Video: https://youtu.content/{vid} | '{title}' at {pub_ist.strftime('%I:%M %p IST')}")
                print(f"   -> BLOCKING ANY DUPLICATE UPLOAD. Strictly 1 video per slot!")
                return True

        return False
    except Exception as e:
        print(f"[!] Live YouTube Guard API Check notice: {e}")
        return False


if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent
    c_token = base / "token.pickle"
    g_token = base / "gaming_bot" / "token.pickle"
    
    print("Cosmic Posted Morning?", has_channel_posted_in_slot(c_token, "morning"))
    print("Gaming Posted Afternoon?", has_channel_posted_in_slot(g_token, "afternoon"))
