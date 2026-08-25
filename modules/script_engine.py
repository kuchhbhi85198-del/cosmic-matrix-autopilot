import os
import re
import sys
import json
import random
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCRIPTS_DIR = Path("E:/MY DATA/FULL SRCCIPT")
BASE_DIR = Path(__file__).resolve().parent.parent
HISTORY_FILE = BASE_DIR / "logs" / "used_scripts_history.json"

NOISE_PATTERNS = [
    r'^(भाई|अरे भाई|प्रदीप भाई|राठौर भाई|सुन भाई|नमस्ते|हेलो|हाय)[,\s!.]*',
    r'^(Bhai|Are bhai|Pradeep bhai|Rathour bhai|Sun bhai|Hello|Hi)[,\s!.]*',
    r'आपने जो बात कही है ना, वह सीधे',
    r'आपने जो कहा ना कि',
    r'तुमने तो विज्ञान के सबसे कड़े',
    r'कसम से, आज आपकी इस बात ने रोंगटे खड़े कर दिए',
    r'बिल्कुल 100% परम सत्य पर आकर आपकी यह पूरी खोज मुकम्मल हुई है',
    r'खत्म... टाटा... बाय-बाय!',
    r'आइए आपके इस अंतिम महा-निष्कर्ष को',
    r'चलो तुम्हारी इस .* थ्योरी को',
    r'ज़रा इस बात की गहराई और इस तीखे रोस्ट को महसूस कीजिए'
]

class CosmicScriptEngine:
    def __init__(self):
        self.docx_files = sorted(list(SCRIPTS_DIR.glob("*.docx")))
        self.used_scripts = self._load_history()

    def _load_history(self) -> list:
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def _save_history(self, filename: str):
        self.used_scripts.append(filename)
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.used_scripts, f, indent=2)

    def _read_docx(self, path: Path) -> str:
        try:
            with zipfile.ZipFile(path) as z:
                xml_content = z.read('word/document.xml')
                tree = ET.fromstring(xml_content)
                texts = [node.text for node in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text]
                return ''.join(texts)
        except Exception:
            return ""

    def _clean_text(self, raw: str) -> str:
        text = raw
        for p in NOISE_PATTERNS:
            text = re.sub(p, '', text, flags=re.IGNORECASE)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def get_next_pro_script(self) -> dict:
        """
        Picks the next un-used script from the 726 library, cleans noise,
        and creates a high-impact 30-45s viral reel narration & headlines.
        """
        available = [f for f in self.docx_files if f.name not in self.used_scripts]
        if not available:
            self.used_scripts = []
            available = self.docx_files

        chosen_file = random.choice(available[:30])
        raw = self._read_docx(chosen_file)
        cleaned = self._clean_text(raw)

        # Extract first 2-3 impactful sentences (around 200-300 characters for 25-35s voice)
        sentences = [s.strip() for s in re.split(r'[।?!]+', cleaned) if len(s.strip()) > 15]
        
        narration_parts = []
        cur_len = 0
        for s in sentences:
            if cur_len + len(s) < 320:
                narration_parts.append(s)
                cur_len += len(s)
            else:
                break
        
        narration = '। '.join(narration_parts) + '।'
        
        # Derive catchy top hook and topic
        title_raw = chosen_file.name.replace(".docx", "").replace("_", " ").strip()
        top_hook = title_raw[:35] + " 🌌"
        
        topic_tag = "COSMIC MATRIX DECODED"
        if "समय" in cleaned or "time" in cleaned.lower() or "ब्लॉक" in cleaned:
            topic_tag = "BLOCK UNIVERSE & TIME"
        elif "परमाणु" in cleaned or "atom" in cleaned.lower() or "प्यार" in cleaned:
            topic_tag = "ATOMIC FORCE & LOVE"
        elif "दिमाग" in cleaned or "brain" in cleaned.lower() or "फ्रीक्वेंसी" in cleaned:
            topic_tag = "BRAIN ANTENNA (432 Hz)"
        elif "माया" in cleaned or "सिमुलेशन" in cleaned or "matrix" in cleaned.lower():
            topic_tag = "THE SIMULATION MATRIX"

        self._save_history(chosen_file.name)

        return {
            "source_file": chosen_file.name,
            "narration": narration,
            "top_hook": top_hook,
            "topic_tag": topic_tag
        }

if __name__ == "__main__":
    engine = CosmicScriptEngine()
    data = engine.get_next_pro_script()
    print("Source:", data["source_file"])
    print("Top Hook:", data["top_hook"])
    print("Topic Tag:", data["topic_tag"])
    print("Narration:", data["narration"])
