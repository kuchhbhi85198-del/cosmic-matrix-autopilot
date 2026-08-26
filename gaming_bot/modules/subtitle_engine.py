import re
from pathlib import Path
from config import (
    VIDEO_WIDTH, VIDEO_HEIGHT, DEFAULT_FONT_SIZE, 
    DEFAULT_FONT_COLOR, DEFAULT_STROKE_COLOR, DEFAULT_STROKE_WIDTH
)

class SubtitleEngine:
    def __init__(self):
        pass

    def srt_to_ass(self, srt_path: Path, ass_path: Path) -> Path:
        """
        Converts SRT file into a stylish ASS (Advanced SubStation Alpha) subtitle file
        tailored for 9:16 Shorts with centered bold text, black outline, and bright font.
        """
        if not srt_path.exists():
            raise FileNotFoundError(f"SRT file not found: {srt_path}")

        ass_header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {VIDEO_WIDTH}
PlayResY: {VIDEO_HEIGHT}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial Black,{DEFAULT_FONT_SIZE},&H0000FFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,{DEFAULT_STROKE_WIDTH},2,2,40,40,300,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        with open(srt_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Parse SRT blocks
        pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n((?:(?!\n\n).)*)', re.DOTALL)
        matches = pattern.findall(content)

        events = []
        for match in matches:
            idx, start, end, text = match
            # Convert SRT time (00:00:01,234) to ASS time (0:00:01.23)
            def fmt_time(t_str):
                t_str = t_str.replace(',', '.')
                parts = t_str.split(':')
                h = int(parts[0])
                m = parts[1]
                s = parts[2][:5]
                return f"{h}:{m}:{s}"

            start_ass = fmt_time(start)
            end_ass = fmt_time(end)
            clean_text = text.replace('\n', ' ').strip().upper()
            
            # Highlight with ASS formatting tags
            formatted_text = r"{\fad(100,100)}" + clean_text
            events.append(f"Dialogue: 0,{start_ass},{end_ass},Default,,0,0,0,,{formatted_text}")

        with open(ass_path, "w", encoding="utf-8") as f:
            f.write(ass_header + "\n".join(events) + "\n")

        return ass_path


if __name__ == "__main__":
    sub_engine = SubtitleEngine()
    print("SubtitleEngine initialized successfully.")
