import base64
import sys
from pathlib import Path

# Ensure UTF-8 output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent

TOKEN_PICKLE = BASE_DIR / "token.pickle"
CLIENT_SECRET = BASE_DIR / "client_secret.json"
INSTA_SESSION = BASE_DIR / "instagram_session.json"
ENV_FILE = BASE_DIR / ".env"


def export_secrets():
    print("=" * 70)
    print("GITHUB ACTIONS SECRETS FOR COSMIC MATRIX BOT (COPY-PASTE)")
    print("=" * 70)

    # 1. TOKEN_PICKLE_BASE64
    if TOKEN_PICKLE.exists():
        with open(TOKEN_PICKLE, "rb") as f:
            b64_token = base64.b64encode(f.read()).decode("utf-8")
        print("\n[SECRET #1] Name: TOKEN_PICKLE_BASE64")
        print("Value:")
        print(b64_token)
    else:
        print("\n[!] token.pickle not found!")

    # 2. CLIENT_SECRET_JSON
    if CLIENT_SECRET.exists():
        with open(CLIENT_SECRET, "r", encoding="utf-8") as f:
            cs_content = f.read()
        print("\n[SECRET #2] Name: CLIENT_SECRET_JSON")
        print("Value:")
        print(cs_content.strip())
    else:
        print("\n[!] client_secret.json not found!")

    # 3. INSTAGRAM_SESSION
    if INSTA_SESSION.exists():
        with open(INSTA_SESSION, "r", encoding="utf-8") as f:
            insta_content = f.read()
        print("\n[SECRET #3] Name: INSTAGRAM_SESSION")
        print("Value:")
        print(insta_content.strip())
    else:
        print("\n[!] instagram_session.json not found!")

    # 4. X (Twitter) Secrets
    import dotenv
    import os
    dotenv.load_dotenv(ENV_FILE)
    print("\n[SECRET #4] Name: X_API_KEY")
    print("Value:", os.getenv("X_API_KEY", ""))
    print("\n[SECRET #5] Name: X_API_SECRET")
    print("Value:", os.getenv("X_API_SECRET", ""))
    print("\n[SECRET #6] Name: X_ACCESS_TOKEN")
    print("Value:", os.getenv("X_ACCESS_TOKEN", ""))
    print("\n[SECRET #7] Name: X_ACCESS_TOKEN_SECRET")
    print("Value:", os.getenv("X_ACCESS_TOKEN_SECRET", ""))

    print("\n" + "=" * 70)
    print("Add these in: GitHub Repo -> Settings -> Secrets and variables -> Actions")
    print("=" * 70)


if __name__ == "__main__":
    export_secrets()
