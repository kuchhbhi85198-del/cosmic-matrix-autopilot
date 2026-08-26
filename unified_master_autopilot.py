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

# Calculate current IST time accurately (UTC + 5:30)
utc_now = datetime.now(timezone.utc)
ist_now = utc_now + timedelta(hours=5, minutes=30)
current_hour_ist = ist_now.hour
current_minute_ist = ist_now.minute

print("=" * 70)
print(f"🌟 [UNIFIED 24/7 MASTER CLOUD AUTOPILOT] IST Time: {ist_now.strftime('%Y-%m-%d %H:%M:%S')} (Hour: {current_hour_ist})")
print("=" * 70)


def run_cosmic_cycle():
    print("\n🚀 [TRIGGERING COSMIC MATRIX BOT (2X DAILY)]...")
    try:
        cmd = [sys.executable, str(BASE_DIR / "autopilot.py"), "--privacy", "public"]
        res = subprocess.run(cmd, cwd=str(BASE_DIR), text=True)
        print(f"[*] Cosmic Bot Completed with Exit Code: {res.returncode}")
    except Exception as e:
        print(f"[!] Cosmic Bot Execution Error: {e}")


def run_gaming_cycle():
    print("\n🎮 [TRIGGERING GAMING/VIRAL REELS BOT (3X DAILY)]...")
    try:
        gaming_script = BASE_DIR / "gaming_bot" / "autopilot.py"
        gaming_cwd = BASE_DIR / "gaming_bot"
        cmd = [sys.executable, str(gaming_script), "--privacy", "public"]
        res = subprocess.run(cmd, cwd=str(gaming_cwd), text=True)
        print(f"[*] Gaming Bot Completed with Exit Code: {res.returncode}")
    except Exception as e:
        print(f"[!] Gaming Bot Execution Error: {e}")


def main():
    # Slot 1: Morning (04:00 - 11:59 IST) -> Run BOTH Cosmic (1) + Gaming (1)
    if 4 <= current_hour_ist < 12:
        print("[SLOT DETECTED: MORNING (09:00 AM IST)] -> Running Cosmic 1 + Gaming 1")
        run_cosmic_cycle()
        run_gaming_cycle()

    # Slot 2: Afternoon (12:00 - 16:59 IST) -> Run Gaming (2) (2:00 PM)
    elif 12 <= current_hour_ist < 17:
        print("[SLOT DETECTED: AFTERNOON (02:00 PM IST)] -> Running Gaming 2")
        run_gaming_cycle()

    # Slot 3: Evening Prime (17:00 - 18:59 IST) -> Run Cosmic (2) (6:00 PM)
    elif 17 <= current_hour_ist < 19:
        print("[SLOT DETECTED: EVENING PRIME (06:00 PM IST)] -> Running Cosmic 2")
        run_cosmic_cycle()

    # Slot 4: Night Prime (19:00 - 23:59 IST) -> Run Gaming (3) (7:00 PM)
    else:
        print("[SLOT DETECTED: NIGHT PRIME (07:00 PM IST)] -> Running Gaming 3")
        run_gaming_cycle()

    print("\n" + "=" * 70)
    print(f"✅ [MASTER CLOUD AUTOPILOT DISPATCH COMPLETE] Next slot will run on schedule!")
    print("=" * 70)


if __name__ == "__main__":
    main()
