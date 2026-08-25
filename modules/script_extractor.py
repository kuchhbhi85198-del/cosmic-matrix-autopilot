import re
import sys
import json
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
OUTPUT_JSON = Path("D:/WORKING/AUTOPILOT_BOTS/cosmic_matrix_bot/assets/cleaned_726_science_scripts.json")

def read_docx(path: Path) -> str:
    try:
        with zipfile.ZipFile(path) as z:
            xml_content = z.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            texts = [node.text for node in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text]
            return ''.join(texts)
    except Exception:
        return ""

def is_pure_science_sentence(s: str) -> bool:
    bad_words = [
        "भाई", "आपने", "आपकी", "तुम्हारा", "तुम्हारी", "राठौर", "कसम से", "मुकम्मल",
        "रोस्ट", "नमस्ते", "दिल खुश", "बधाई", "खत्म... टाटा", "प्रदीप", "तूने", "तुमने",
        "अरे भाई", "सुन भाई", "रमेश", "राठौर भाई", "प्रदीप भाई", "लाजवाब है"
    ]
    for w in bad_words:
        if w in s:
            return False
    return len(s) > 25

def process_all_scripts():
    files = sorted(list(SCRIPTS_DIR.glob("*.docx")))
    master_library = []

    for f in files:
        raw = read_docx(f)
        sentences = [s.strip() for s in re.split(r'[।?!]+', raw) if len(s.strip()) > 20]
        
        # Filter for pure factual science sentences only
        factual_sentences = [s for s in sentences if is_pure_science_sentence(s)]
        
        if len(factual_sentences) < 2:
            continue
            
        script_parts = []
        cur_len = 0
        for s in factual_sentences:
            if cur_len + len(s) < 280:
                script_parts.append(s)
                cur_len += len(s)
            else:
                break
                
        if len(script_parts) < 2:
            continue
            
        final_narration = '। '.join(script_parts) + '।'
        
        # Professional Science Headlines
        headline = "ब्रह्मांड का वैज्ञानिक रहस्य 🌌"
        tag = "PURE SCIENCE & UNIVERSE"
        
        if "न्यूरो" in final_narration or "केमिकल" in final_narration or "दिमाग" in final_narration or "कोर्टिसोल" in final_narration or "एड्रेनालाईन" in final_narration:
            headline = "दिमाग के केमिकल्स का रहस्य 🧠"
            tag = "NEUROSCIENCE & CHEMICALS"
        elif "इलेक्ट्रोस्टैटिक" in final_narration or "परमाणु" in final_narration or "इलेक्ट्रॉन" in final_narration or "बॉन्ड" in final_narration:
            headline = "परमाणुओं का असली बल ⚛️"
            tag = "ATOMIC FORCE & PHYSICS"
        elif "समय" in final_narration or "सापेक्षता" in final_narration or "ब्लॉक" in final_narration or "आइंस्टीन" in final_narration:
            headline = "समय का असली सच क्या है? ⏳"
            tag = "TIME & RELATIVITY"
        elif "क्वांटम" in final_narration or "तरंग" in final_narration or "ऑब्जर्वर" in final_narration:
            headline = "क्वांटम रियलिटी का रहस्य 👁️"
            tag = "QUANTUM PHYSICS"
        elif "सिमुलेशन" in final_narration or "सिग्नल" in final_narration or "माया" in final_narration:
            headline = "क्या ब्रह्मांड एक सिमुलेशन है? 💻"
            tag = "THE SIMULATION MATRIX"

        master_library.append({
            "id": len(master_library) + 1,
            "source_file": f.name,
            "headline": headline,
            "tag": tag,
            "narration": final_narration
        })

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(master_library, f, ensure_ascii=False, indent=2)

    print(f"🎉 [SUCCESS] Cleaned and Extracted {len(master_library)} 100% PURE Science Scripts to {OUTPUT_JSON}!")

if __name__ == "__main__":
    process_all_scripts()
