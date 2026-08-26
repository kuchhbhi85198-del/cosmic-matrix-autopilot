import subprocess
from pathlib import Path
import imageio_ffmpeg
from config import ASSETS_DIR

SFX_DIR = ASSETS_DIR / "sfx"
SFX_DIR.mkdir(parents=True, exist_ok=True)


class SFXManager:
    def __init__(self):
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        self.ensure_default_sfx()

    def ensure_default_sfx(self):
        """
        Generates standard high-energy SFX (Whoosh, Bass Drop, Impact, Hit)
        using FFmpeg audio synthesis if custom files are not present.
        """
        whoosh_file = SFX_DIR / "whoosh.wav"
        bassdrop_file = SFX_DIR / "bass_drop.wav"
        impact_file = SFX_DIR / "impact.wav"

        # 1. Whoosh SFX (Synthesized sweep with white noise + bandpass filter)
        if not whoosh_file.exists():
            cmd = [
                self.ffmpeg_exe, "-y",
                "-f", "lavfi",
                "-i", "anoisesrc=d=0.4:c=white:r=44100:a=0.5",
                "-af", "bandpass=f=1200:w=800,afade=t=in:ss=0:d=0.2,afade=t=out:st=0.2:d=0.2,volume=1.5",
                str(whoosh_file)
            ]
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 2. Bass Drop / Sub-bass Hit (Synthesized low sine frequency sweep)
        if not bassdrop_file.exists():
            cmd = [
                self.ffmpeg_exe, "-y",
                "-f", "lavfi",
                "-i", "sine=f=120:d=0.8:r=44100",
                "-af", "asetrate=44100*0.7,aresample=44100,afade=t=in:ss=0:d=0.05,afade=t=out:st=0.1:d=0.7,volume=2.0",
                str(bassdrop_file)
            ]
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 3. Impact / Hit (Punchy attack + decay)
        if not impact_file.exists():
            cmd = [
                self.ffmpeg_exe, "-y",
                "-f", "lavfi",
                "-i", "sine=f=200:d=0.5:r=44100",
                "-af", "asetrate=44100*0.5,aresample=44100,afade=t=in:ss=0:d=0.02,afade=t=out:st=0.05:d=0.45,volume=2.2",
                str(impact_file)
            ]
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def get_sfx(self, sfx_type: str = "whoosh") -> Path:
        """Returns path to requested SFX."""
        file_map = {
            "whoosh": SFX_DIR / "whoosh.wav",
            "bass_drop": SFX_DIR / "bass_drop.wav",
            "impact": SFX_DIR / "impact.wav"
        }
        return file_map.get(sfx_type, SFX_DIR / "whoosh.wav")


if __name__ == "__main__":
    mgr = SFXManager()
    print("SFX files generated in:", SFX_DIR)
