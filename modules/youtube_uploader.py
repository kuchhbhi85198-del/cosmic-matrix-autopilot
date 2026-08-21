import pickle
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from config import YOUTUBE_CLIENT_SECRET, YOUTUBE_TOKEN_PICKLE


class YouTubeUploader:
    def __init__(self):
        self.scopes = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.readonly"]
        self.youtube = self._authenticate()

    def _authenticate(self):
        creds = None
        if YOUTUBE_TOKEN_PICKLE.exists():
            with open(YOUTUBE_TOKEN_PICKLE, "rb") as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                with open(YOUTUBE_TOKEN_PICKLE, "wb") as token:
                    pickle.dump(creds, token)
            elif YOUTUBE_CLIENT_SECRET.exists():
                flow = InstalledAppFlow.from_client_secrets_file(str(YOUTUBE_CLIENT_SECRET), self.scopes)
                creds = flow.run_local_server(port=0)
                with open(YOUTUBE_TOKEN_PICKLE, "wb") as token:
                    pickle.dump(creds, token)

        if creds:
            return build("youtube", "v3", credentials=creds)
        return None

    def upload_short(self, video_path: Path, title: str, description: str, tags: list, privacy: str = "public") -> dict:
        if not self.youtube:
            return {"status": "skipped", "message": "YouTube not authenticated (token.pickle missing)"}

        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": "28" # Science & Technology / Gaming
            },
            "status": {
                "privacyStatus": privacy,
                "selfDeclaredMadeForKids": False
            }
        }

        media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True, mimetype="video/mp4")
        request = self.youtube.videos().insert(part="snippet,status", body=body, media_body=media)

        response = None
        while response is None:
            status, response = request.next_chunk()

        video_id = response.get("id")
        return {
            "status": "success",
            "video_id": video_id,
            "url": f"https://youtu.be/{video_id}"
        }
