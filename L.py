import sys
from pathlib import Path
from instagrapi import Client

BASE_DIR = Path(__file__).resolve().parent
SESSION_FILE = BASE_DIR / "instagram_session.json"


def login_new_instagram():
    print("=" * 65)
    print("📸 NEW INSTAGRAM ACCOUNT LOGIN (COSMIC MATRIX)")
    print("=" * 65)
    print("Enter the Username and Password for your NEW Instagram Account:")
    
    username = input("👉 New Instagram Username: ").strip()
    password = input("👉 New Instagram Password: ").strip()

    if not username or not password:
        print("[!] Username or Password cannot be empty!")
        return

    cl = Client()
    try:
        print(f"[*] Logging in to @{username}...")
        cl.login(username, password)
        cl.dump_settings(SESSION_FILE)
        print("=" * 65)
        print(f"🎉 [SUCCESS] Connected to NEW Instagram: @{username}!")
        print(f"✅ Session saved to: {SESSION_FILE}")
        print("=" * 65)
    except Exception as e:
        print(f"\n[!] Login notice: {e}")
        sessionid = input("\n👉 If 2FA blocked, paste your new account's 'sessionid' cookie here: ").strip()
        if sessionid:
            try:
                cl.login_by_sessionid(sessionid)
                cl.dump_settings(SESSION_FILE)
                print(f"🎉 [SUCCESS] Logged in via sessionid! Saved to {SESSION_FILE}")
            except Exception as ex:
                print(f"[!] Error: {ex}")


if __name__ == "__main__":
    login_new_instagram()
