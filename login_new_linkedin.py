import os
import sys
import webbrowser
import requests
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"


class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if "code" in params:
            self.server.auth_code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("<h1>🎉 LinkedIn Login Successful! You can close this tab now.</h1>".encode("utf-8"))
        else:
            self.send_response(400)
            self.end_headers()


def connect_linkedin():
    print("=" * 65)
    print("💼 CONNECT LINKEDIN ACCOUNT (COSMIC MATRIX)")
    print("=" * 65)

    client_id = input("👉 Enter LinkedIn Client ID: ").strip()
    client_secret = input("👉 Enter LinkedIn Client Secret: ").strip()

    if not client_id or not client_secret:
        print("[!] Client ID or Client Secret cannot be empty!")
        return

    redirect_uri = "http://localhost:8080/callback"
    scope = "openid profile email w_member_social"

    auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization?"
        f"response_type=code&client_id={client_id}&"
        f"redirect_uri={urllib.parse.quote(redirect_uri)}&"
        f"scope={urllib.parse.quote(scope)}"
    )

    print("\n[*] Opening browser to authorize LinkedIn...")
    webbrowser.open(auth_url)

    server = HTTPServer(("localhost", 8080), OAuthHandler)
    server.auth_code = None
    print("[*] Waiting for authorization callback...")
    while not server.auth_code:
        server.handle_request()

    code = server.auth_code
    print(f"[*] Exchanging authorization code for Access Token...")

    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret
    }
    res = requests.post(token_url, data=payload)
    token_data = res.json()

    if "access_token" not in token_data:
        print(f"[!] Failed to get access token: {token_data}")
        return

    access_token = token_data["access_token"]

    # Get User Profile URN
    userinfo_url = "https://api.linkedin.com/v2/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_res = requests.get(userinfo_url, headers=headers).json()
    person_urn = user_res.get("sub", "")

    print("=" * 65)
    print(f"🎉 [SUCCESS] Connected to LinkedIn: {user_res.get('name', 'User')} (URN: {person_urn})!")
    print("=" * 65)

    # Save to .env
    dotenv.set_key(str(ENV_FILE), "LINKEDIN_ACCESS_TOKEN", access_token)
    dotenv.set_key(str(ENV_FILE), "LINKEDIN_PERSON_URN", person_urn)
    print(f"✅ Credentials saved to {ENV_FILE}")


if __name__ == "__main__":
    connect_linkedin()
