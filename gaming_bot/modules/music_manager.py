import subprocess
from pathlib import Path
import imageio_ffmpeg
from config import MUSIC_DIR


class MusicManager:
    def __init__(self):
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        self.ensure_default_track()

    def ensure_default_track(self):
        """
        Creates an energetic rhythmic beat track if user hasn't added music files yet.
        """
        default_track = MUSIC_DIR / "hype_beat.wav"
        if not default_track.exists():
            # Generate a 30s rhythmic synth pulse track with drums using FFmpeg synthesis
            cmd = [
                self.ffmpeg_exe, "-y",
                "-f", "lavfi",
                "-i", "sine=f=130:d=30:r=44100",
                "-af", "tremolo=f=4.0:d=0.8,apulsator=mode=sine:hz=2.0,volume=1.0",
                str(default_track)
            ]
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def get_track(self, custom_path: Path = None) -> Path:
        """
        Returns a music track from assets/music or default.
        """
        if custom_path and custom_path.exists():
            return custom_path
            
        tracks = list(MUSIC_DIR.glob("*.mp3")) + list(MUSIC_DIR.glob("*.wav"))
        if tracks:
            return tracks[0]
            
        return MUSIC_DIR / "hype_beat.wav"


if __name__ == "__main__":
    mm = MusicManager()
    print("MusicManager ready. Active track:", mm.get_track())
