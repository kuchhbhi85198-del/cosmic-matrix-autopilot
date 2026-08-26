import os
import sys
import shutil
import sqlite3
import json
import base64
from pathlib import Path

# Ensure root project directory is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import win32crypt
from Cryptodome.Cipher import AES
from instagrapi import Client

SESSION_FILE = BASE_DIR / "instagram_session.json"


def get_edge_key():
    local_state_path = Path(os.environ["LOCALAPPDATA"]) / "Microsoft" / "Edge" / "User Data" / "Local State"
    if not local_state_path.exists():
        return None
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = json.load(f)
    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    encrypted_key = encrypted_key[5:]
    return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]


def decrypt_cookie_val(encrypted_value, key):
    try:
        if encrypted_value.startswith(b'v10') or encrypted_value.startswith(b'v11') or encrypted_value.startswith(b'v20'):
            nonce = encrypted_value[3:15]
            ciphertext = encrypted_value[15:-16]
            tag = encrypted_value[-16:]
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
        else:
            return win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1].decode('utf-8')
    except Exception:
        return None


def extract_and_login():
    print("=" * 65)
    print("🚀 AUTOMATIC INSTAGRAM LOGIN FROM MICROSOFT EDGE")
    print("=" * 65)
    
    edge_dir = Path(os.environ["LOCALAPPDATA"]) / "Microsoft" / "Edge" / "User Data"
    key = get_edge_key()
    
    profiles = ["Default"] + [f.name for f in edge_dir.glob("Profile *")]
    session_id = None
    
    for profile in profiles:
        cookie_file = edge_dir / profile / "Network" / "Cookies"
        if not cookie_file.exists():
            continue
            
        temp_copy = BASE_DIR / f"temp_{profile}_cookies.db"
        try:
            shutil.copy2(cookie_file, temp_copy)
            conn = sqlite3.connect(temp_copy)
            c = conn.cursor()
            c.execute("SELECT name, encrypted_value FROM cookies WHERE host_key LIKE '%instagram.com%'")
            rows = c.fetchall()
            conn.close()
            
            for name, enc_val in rows:
                if name == "sessionid":
                    dec = decrypt_cookie_val(enc_val, key)
                    if dec:
                        session_id = dec
                        print(f"[+] Found sessionid in Edge profile: {profile}")
                        break
        except PermissionError:
            print(f"\n[!] Microsoft Edge is currently open and locking the cookie file.")
            print("[*] Please close Microsoft Edge (all windows) for 5 seconds...")
            input("👉 Press ENTER once you have closed Microsoft Edge: ")
            # Try again
            try:
                shutil.copy2(cookie_file, temp_copy)
                conn = sqlite3.connect(temp_copy)
                c = conn.cursor()
                c.execute("SELECT name, encrypted_value FROM cookies WHERE host_key LIKE '%instagram.com%'")
                rows = c.fetchall()
                conn.close()
                for name, enc_val in rows:
                    if name == "sessionid":
                        dec = decrypt_cookie_val(enc_val, key)
                        if dec:
                            session_id = dec
                            break
            except Exception as e:
                print(f"[!] Error: {e}")
        except Exception as e:
            print(f"[!] Error: {e}")
        finally:
            if temp_copy.exists():
                try:
                    temp_copy.unlink()
                except Exception:
                    pass
                    
        if session_id:
            break

    if not session_id:
        print("\n[!] Could not auto-extract sessionid directly.")
        print("[*] Manual 5-second method:")
        print("    1. Open Edge -> Go to instagram.com -> Press F12")
        print("    2. Go to 'Application' (or Storage) -> Cookies -> https://www.instagram.com")
        print("    3. Copy value of 'sessionid'")
        session_id = input("\n👉 Paste sessionid here: ").strip()

    if session_id:
        print(f"\n[*] Logging into Instagram Client via session ID...")
        try:
            cl = Client()
            cl.login_by_sessionid(session_id)
            cl.dump_settings(SESSION_FILE)
            print("=" * 65)
            print("🎉 [SUCCESS] Instagram Auto-Login Complete & Session Saved!")
            print(f"✅ Saved to: {SESSION_FILE}")
            print("✅ Now Autopilot can upload Reels automatically 24/7!")
            print("=" * 65)
            return True
        except Exception as e:
            print(f"[!] Login failed with provided session: {e}")
            return False

    return False


if __name__ == "__main__":
    extract_and_login()
