import os
import sys
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Ensure UTF-8 console output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from modules.live_youtube_guard import has_channel_posted_in_slot

# Calculate current IST time accurately (UTC + 5:30)
utc_now = datetime.now(timezone.utc)
ist_now = utc_now + timedelta(hours=5, minutes=30)
current_hour_ist = ist_now.hour
current_minute_ist = ist_now.minute

print("=" * 70)
print(f"🌟 [UNIFIED 24/7 MASTER CLOUD AUTOPILOT] IST Time: {ist_now.strftime('%Y-%m-%d %H:%M:%S')} (Hour: {current_hour_ist})")
print("=" * 70)

COSMIC_TOKEN = BASE_DIR / "token.pickle"
GAMING_TOKEN = BASE_DIR / "gaming_bot" / "token.pickle"


def run_cosmic_cycle(slot_name: str):
    if has_channel_posted_in_slot(COSMIC_TOKEN, slot_name):
        print(f"[*] 🛑 [SLOT GUARD] Cosmic Channel already has today's {slot_name.upper()} video live! Exiting cleanly.")
        return

    print(f"\n🚀 [TRIGGERING COSMIC MATRIX BOT for {slot_name.upper()}]...")
    try:
        cmd = [sys.executable, str(BASE_DIR / "autopilot.py"), "--privacy", "public"]
        res = subprocess.run(cmd, cwd=str(BASE_DIR), text=True)
        print(f"[*] Cosmic Bot Completed with Exit Code: {res.returncode}")
    except Exception as e:
        print(f"[!] Cosmic Bot Execution Error: {e}")


def run_gaming_cycle(slot_name: str):
    if has_channel_posted_in_slot(GAMING_TOKEN, slot_name):
        print(f"[*] 🛑 [SLOT GUARD] Gaming Channel already has today's {slot_name.upper()} video live! Exiting cleanly.")
        return

    print(f"\n🎮 [TRIGGERING GAMING/VIRAL REELS BOT for {slot_name.upper()}]...")
    try:
        gaming_script = BASE_DIR / "gaming_bot" / "autopilot.py"
        gaming_cwd = BASE_DIR / "gaming_bot"
        cmd = [sys.executable, str(gaming_script), "--privacy", "public"]
        res = subprocess.run(cmd, cwd=str(gaming_cwd), text=True)
        print(f"[*] Gaming Bot Completed with Exit Code: {res.returncode}")
    except Exception as e:
        print(f"[!] Gaming Bot Execution Error: {e}")


def main():
    # Slot 1: Morning Window (08:00 - 11:59 IST) -> Target 09:00 AM IST (Cosmic 1 + Gaming 1)
    if 8 <= current_hour_ist < 12:
        print("[SLOT DETECTED: MORNING WINDOW (09:00 AM IST)] -> Running Cosmic 1 + Gaming 1")
        run_cosmic_cycle("morning")
        run_gaming_cycle("morning")

    # Slot 2: Afternoon Window (13:00 - 16:59 IST) -> Target 02:00 PM IST (Gaming 2)
    elif 13 <= current_hour_ist < 17:
        print("[SLOT DETECTED: AFTERNOON WINDOW (02:00 PM IST)] -> Running Gaming 2")
        run_gaming_cycle("afternoon")

    # Slot 3: Evening Prime (17:00 - 18:59 IST) -> Target 06:00 PM IST (Cosmic 2)
    elif 17 <= current_hour_ist < 19:
        print("[SLOT DETECTED: EVENING PRIME WINDOW (06:00 PM IST)] -> Running Cosmic 2")
        run_cosmic_cycle("evening")

    # Slot 4: Night Prime (19:00 - 22:00 IST) -> Target 07:00 PM IST (Gaming 3)
    elif 19 <= current_hour_ist <= 22:
        print("[SLOT DETECTED: NIGHT PRIME WINDOW (07:00 PM IST)] -> Running Gaming 3")
        run_gaming_cycle("night")

    # Outside Active Slots: SLEEP / DO NOTHING (Late night 22:00 - 08:00 AM IST)
    else:
        print(f"[*] 🌙 [OFF-HOURS SLEEP] Current IST Hour {current_hour_ist}:00 is Outside Posting Windows. Sleeping safely!")

    print("\n" + "=" * 70)
    print("✅ [MASTER CLOUD AUTOPILOT CYCLE COMPLETE]")
    print("=" * 70)


if __name__ == "__main__":
    main()
