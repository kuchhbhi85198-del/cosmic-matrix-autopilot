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
    Direct Live YouTube API Check via Instant Uploads Playlist:
    Queries the actual YouTube Channel's uploads playlist directly (0ms indexing latency)
    to see if any video was already published in the specified slot window today.
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
        
        # 1. Get Instant Uploads Playlist ID
        ch_res = yt.channels().list(part="contentDetails", mine=True).execute()
        if not ch_res.get("items"):
            return False
        uploads_playlist_id = ch_res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        
        # 2. Get latest 10 uploads instantly
        pl_res = yt.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=10
        ).execute()

        ist_now = get_ist_now()
        today_date = ist_now.date()

        # Strict Matching Windows in IST
        if slot_type == "morning":
            slot_start_h, slot_end_h = 7, 12   # Morning: 07:00 AM - 11:59 AM
        elif slot_type == "afternoon":
            slot_start_h, slot_end_h = 12, 17  # Afternoon: 12:00 PM - 04:59 PM
        elif slot_type == "evening":
            slot_start_h, slot_end_h = 17, 19  # Evening: 05:00 PM - 06:59 PM
        elif slot_type == "night":
            slot_start_h, slot_end_h = 19, 23  # Night: 07:00 PM - 10:59 PM
        else:
            slot_start_h, slot_end_h = 0, 24

        for item in pl_res.get("items", []):
            pub_raw = item["contentDetails"].get("videoPublishedAt") or item["snippet"].get("publishedAt")
            if not pub_raw:
                continue
            pub_utc = datetime.fromisoformat(pub_raw.replace("Z", "+00:00"))
            pub_ist = pub_utc.astimezone(IST)

            # If video was published TODAY in this exact slot window
            if pub_ist.date() == today_date and slot_start_h <= pub_ist.hour < slot_end_h:
                title = item["snippet"].get("title", "")
                vid = item["contentDetails"].get("videoId", "")
                print(f"🛑 [LIVE YOUTUBE SHIELD] Found video already live on channel for today's {slot_type.upper()} slot!")
                print(f"   -> Live Video: https://youtu.be/{vid} | '{title}' at {pub_ist.strftime('%I:%M %p IST')}")
                print(f"   -> STRICTLY 1 VIDEO PER SLOT ENFORCED. Blocking duplicate upload.")
                return True

        return False
    except Exception as e:
        print(f"[!] Live YouTube Shield Check notice: {e}")
        return False
