import os
import sys
import pickle
import webbrowser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

CLIENT_SECRETS_FILE = BASE_DIR / "client_secret.json"
TOKEN_FILE = BASE_DIR / "token.pickle"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.readonly"]
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def login_new_youtube():
    print("=" * 65)
    print("📺 LOGIN NEW YOUTUBE CHANNEL (COSMIC MATRIX)")
    print("=" * 65)

    if not CLIENT_SECRETS_FILE.exists():
        print("\n[!] Please place your Google Cloud 'client_secret.json' in this folder first!")
        print(f"👉 Target Folder: {BASE_DIR}")
        return

    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS_FILE), SCOPES)
    if os.path.exists(CHROME_PATH):
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(CHROME_PATH))
        print("[*] Opening Google Chrome to select your NEW YouTube Channel...")
        creds = flow.run_local_server(port=0, browser='chrome')
    else:
        creds = flow.run_local_server(port=0)

    with open(TOKEN_FILE, "wb") as token:
        pickle.dump(creds, token)

    try:
        youtube = build("youtube", "v3", credentials=creds)
        response = youtube.channels().list(mine=True, part="snippet").execute()
        if "items" in response and response["items"]:
            ch_title = response["items"][0]["snippet"]["title"]
            print("=" * 65)
            print(f"🎉 [SUCCESS] Connected to NEW Channel: '{ch_title}'!")
            print(f"✅ Token saved to: {TOKEN_FILE}")
            print("=" * 65)
    except Exception as e:
        print(f"[*] Channel notice: {e}")


if __name__ == "__main__":
    login_new_youtube()
