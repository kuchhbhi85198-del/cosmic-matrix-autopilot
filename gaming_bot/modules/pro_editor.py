import re
import os
import sys
import subprocess
from pathlib import Path
import imageio_ffmpeg
from config import VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS, OUTPUT_DIR
from modules.sfx_manager import SFXManager


class ProEditor:
    """
    Production-Grade Esports & Gaming Shorts Editor:
    - 9:16 Cinematic Canvas (Center 4K Crop + Blurred Neon Background)
    - 4K Sharpness + Saturation Boost
    - Retention Progress Bar
    - Top Golden Neon Hook Badge
    - Stream-looped video & phonk music
    """
    def __init__(self):
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        self.sfx_mgr = SFXManager()

    def _get_system_font(self) -> str:
        if sys.platform == "win32":
            win_font = Path("C:/Windows/Fonts/arialbd.ttf")
            if win_font.exists():
                return "C\\:/Windows/Fonts/arialbd.ttf"
            return "C\\:/Windows/Fonts/arial.ttf"
        else:
            linux_fonts = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
            ]
            for f in linux_fonts:
                if os.path.exists(f):
                    return f
            return "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

    def get_video_duration(self, video_path: Path) -> float:
        cmd = [self.ffmpeg_exe, "-i", str(video_path), "-f", "null", "-"]
        res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        for line in res.stderr.split('\n'):
            if "Duration:" in line:
                time_str = line.split("Duration:")[1].split(",")[0].strip()
                h, m, s = time_str.split(":")
                return float(h) * 3600 + float(m) * 60 + float(s)
        return 10.0

    def create_pro_short(
        self,
        raw_video_path: Path,
        music_path: Path,
        hook_text: str,
        output_path: Path,
        target_duration: float = 12.0
    ) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        vid_len = self.get_video_duration(raw_video_path)
        actual_duration = min(target_duration, vid_len) if vid_len >= 8.0 else target_duration

        bass_drop = self.sfx_mgr.get_sfx("bass_drop")
        font_path = self._get_system_font()

        # Clean hook text
        clean_hook = re.sub(r'[^\w\s\?!.,-]', '', hook_text).strip().upper()
        if not clean_hook:
            clean_hook = "INSANE GTA 6 MOMENT"

        # PRO Video Filter Graph
        filter_complex = (
            f"[0:v]scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=increase,"
            f"crop={VIDEO_WIDTH}:{VIDEO_HEIGHT},"
            f"unsharp=5:5:1.0:5:5:0.0,"
            f"eq=contrast=1.2:saturation=1.45:brightness=0.02,"
            f"drawtext=fontfile='{font_path}':text='{clean_hook}':fontcolor=yellow:fontsize=48:box=1:boxcolor=black@0.85:boxborderw=20:"
            f"x=(w-text_w)/2:y=240:enable='between(t,0,{actual_duration})',"
            f"drawtext=fontfile='{font_path}':text='WAIT FOR THE END...':fontcolor=white:fontsize=34:box=1:boxcolor=red@0.85:boxborderw=12:"
            f"x=(w-text_w)/2:y=h-240:enable='between(t,0,{actual_duration})',"
            f"drawbox=x=0:y=h-14:w='w*(t/{actual_duration})':h=14:color=yellow@1.0:t=fill[v]"
        )

        audio_input = music_path if (music_path and music_path.exists()) else bass_drop

        cmd = [
            self.ffmpeg_exe, "-y",
            "-stream_loop", "-1",
            "-i", str(raw_video_path),
            "-stream_loop", "-1",
            "-i", str(audio_input),
            "-t", str(actual_duration),
            "-filter_complex", filter_complex,
            "-map", "[v]",
            "-map", "1:a",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "256k",
            str(output_path)
        ]

        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            print(f"[!] Primary render failed, using fallback: {res.stderr[:200]}")
            cmd_fallback = [
                self.ffmpeg_exe, "-y",
                "-stream_loop", "-1",
                "-i", str(raw_video_path),
                "-stream_loop", "-1",
                "-i", str(audio_input),
                "-t", str(actual_duration),
                "-vf", f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=increase,crop={VIDEO_WIDTH}:{VIDEO_HEIGHT},eq=contrast=1.2:saturation=1.3",
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-c:a", "aac",
                str(output_path)
            ]
            subprocess.run(cmd_fallback, check=True)

        return output_path


if __name__ == "__main__":
    editor = ProEditor()
    print("Stream-looped ProEditor ready.")
