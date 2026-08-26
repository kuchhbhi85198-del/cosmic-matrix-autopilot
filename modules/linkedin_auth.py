import os
import sys
import urllib.parse
import requests
from pathlib import Path
from dotenv import load_dotenv

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET", "")
REDIRECT_URI = "https://oauth.pstmn.io/v1/callback"

def get_authorization_url() -> str:
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile email w_member_social",
        "state": "cosmic_matrix_state_123"
    }
    return f"https://www.linkedin.com/oauth/v2/authorization?{urllib.parse.urlencode(params)}"

def exchange_code_for_token(code: str) -> dict:
    url = "https://www.linkedin.com/oauth/v2/accessToken"
    payload = {
        "grant_type": "authorization_code",
        "code": code.strip(),
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    res = requests.post(url, data=payload, headers=headers)
    return res.json()

def get_user_profile(access_token: str) -> dict:
    url = "https://api.linkedin.com/v2/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    res = requests.get(url, headers=headers)
    return res.json()

if __name__ == "__main__":
    print("=" * 60)
    print("LINKEDIN 1-CLICK AUTHENTICATION GENERATOR")
    print("=" * 60)
    print("\n👉 STEP 1: Open this URL in your browser to Authorize:")
    print(get_authorization_url())
    print("=" * 60)
