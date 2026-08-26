import os
from pathlib import Path
from typing import List
from config import YOUTUBE_CLIENT_SECRETS_FILE, YOUTUBE_OAUTH_TOKEN_FILE


class YouTubeUploader:
    def __init__(self):
        self.scopes = ["https://www.googleapis.com/auth/youtube.upload"]

    def upload_short(
        self,
        video_path: Path,
        title: str,
        description: str,
        tags: List[str] = None,
        privacy_status: str = "private"  # 'private', 'unlisted', or 'public'
    ) -> bool:
        """
        Uploads a generated short to YouTube.
        Requires client_secret.json in the project root.
        """
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")

        if not YOUTUBE_CLIENT_SECRETS_FILE.exists():
            print("\n[!] 'client_secret.json' not found in project directory.")
            print("[*] To enable auto-upload to YouTube:")
            print("    1. Go to Google Cloud Console -> APIs & Services -> Credentials")
            print("    2. Create OAuth 2.0 Client ID (Desktop App)")
            print(f"    3. Download JSON and save as: {YOUTUBE_CLIENT_SECRETS_FILE}")
            print(f"[*] Video is saved locally at: {video_path}\n")
            return False

        try:
            import pickle
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload

            creds = None
            if YOUTUBE_OAUTH_TOKEN_FILE.exists():
                with open(YOUTUBE_OAUTH_TOKEN_FILE, "rb") as token:
                    creds = pickle.load(token)

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(YOUTUBE_CLIENT_SECRETS_FILE), self.scopes
                    )
                    creds = flow.run_local_server(port=0)
                with open(YOUTUBE_OAUTH_TOKEN_FILE, "wb") as token:
                    pickle.dump(creds, token)

            youtube = build("youtube", "v3", credentials=creds)

            body = {
                "snippet": {
                    "title": title[:100],
                    "description": description,
                    "tags": tags or ["Shorts", "GTA6", "Gaming"],
                    "categoryId": "20"  # 20 = Gaming
                },
                "status": {
                    "privacyStatus": privacy_status,
                    "selfDeclaredMadeForKids": False
                }
            }

            media = MediaFileUpload(
                str(video_path),
                chunksize=-1,
                resumable=True,
                mimetype="video/mp4"
            )

            print(f"[*] Uploading '{title}' to YouTube ({privacy_status})...")
            request = youtube.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media
            )
            response = request.execute()
            video_id = response.get("id")
            print(f"[SUCCESS] Uploaded to YouTube! URL: https://youtu.be/{video_id}")
            return True

        except Exception as e:
            print(f"[Error] YouTube upload failed: {e}")
            return False


if __name__ == "__main__":
    uploader = YouTubeUploader()
    print("YouTubeUploader ready.")
