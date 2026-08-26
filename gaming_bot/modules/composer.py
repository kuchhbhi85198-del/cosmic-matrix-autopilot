import subprocess
from pathlib import Path
import imageio_ffmpeg
from config import MUSIC_DIR, OUTPUT_DIR


class VideoComposer:
    def __init__(self):
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    def get_audio_duration(self, audio_path: Path) -> float:
        """
        Retrieves duration of audio file in seconds.
        """
        cmd = [
            self.ffmpeg_exe,
            "-i", str(audio_path),
            "-f", "null", "-"
        ]
        res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        # Parse duration from ffmpeg stderr
        for line in res.stderr.split('\n'):
            if "Duration:" in line:
                # Duration: 00:00:15.34, ...
                time_str = line.split("Duration:")[1].split(",")[0].strip()
                h, m, s = time_str.split(":")
                return float(h) * 3600 + float(m) * 60 + float(s)
        return 15.0

    def compose(
        self,
        video_path: Path,
        audio_path: Path,
        ass_subtitle_path: Path,
        output_path: Path,
        music_path: Path = None
    ) -> Path:
        """
        Merges video, voiceover, styled ASS subtitles, and background music into a final MP4 Short.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Format ASS path for FFmpeg filter on Windows
        escaped_ass_path = str(ass_subtitle_path).replace("\\", "/").replace(":", "\\:")
        
        # Audio filter: Mix voice with background music if available
        bg_music = music_path or (list(MUSIC_DIR.glob("*.mp3"))[0] if list(MUSIC_DIR.glob("*.mp3")) else None)
        
        if bg_music and bg_music.exists():
            # Voice at 1.0 volume, background music ducked at 0.12 volume
            cmd = [
                self.ffmpeg_exe,
                "-y",
                "-i", str(video_path),
                "-i", str(audio_path),
                "-stream_loop", "-1",
                "-i", str(bg_music),
                "-filter_complex",
                f"[0:v]subtitles='{escaped_ass_path}'[v];"
                f"[1:a]volume=1.0[v_aud];"
                f"[2:a]volume=0.12[m_aud];"
                f"[v_aud][m_aud]amix=inputs=2:duration=first:dropout_transition=2[a]",
                "-map", "[v]",
                "-map", "[a]",
                "-c:v", "libx264",
                "-preset", "fast",
                "-c:a", "aac",
                "-b:a", "192k",
                "-shortest",
                str(output_path)
            ]
        else:
            # Voice only
            cmd = [
                self.ffmpeg_exe,
                "-y",
                "-i", str(video_path),
                "-i", str(audio_path),
                "-filter_complex", f"[0:v]subtitles='{escaped_ass_path}'[v]",
                "-map", "[v]",
                "-map", "1:a",
                "-c:v", "libx264",
                "-preset", "fast",
                "-c:a", "aac",
                "-b:a", "192k",
                "-shortest",
                str(output_path)
            ]

        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            # Fallback without subtitles if subtitle filter is not supported in minimal build
            print(f"[Warning] Subtitle burning error: {res.stderr[:200]}... Trying direct merge.")
            cmd_fallback = [
                self.ffmpeg_exe,
                "-y",
                "-i", str(video_path),
                "-i", str(audio_path),
                "-map", "0:v",
                "-map", "1:a",
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",
                str(output_path)
            ]
            subprocess.run(cmd_fallback, check=True)

        return output_path


if __name__ == "__main__":
    composer = VideoComposer()
    print("VideoComposer ready.")
