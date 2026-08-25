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

# Strict scientific filters to remove all conversational names, greetings, and AI chat
NOISE_PATTERNS = [
    r'^(भाई|अरे भाई|प्रदीप भाई|राठौर भाई|सुन भाई|नमस्ते|हेलो|हाय|रमेश भाई|भाई रमेश|भाई जी)[,\s!.]*',
    r'^(Bhai|Are bhai|Pradeep bhai|Rathour bhai|Sun bhai|Hello|Hi|Ramesh bhai|Bhai ji)[,\s!.]*',
    r'आपने जो बात कही है ना[,\s]*वह सीधे',
    r'आपने जो कहा ना कि',
    r'तुमने तो विज्ञान के सबसे कड़े',
    r'कसम से[,\s]*आज आपकी (आँखों|बातों) से',
    r'बिल्कुल 100% परम सत्य पर आकर आपकी यह पूरी खोज मुकम्मल हुई है',
    r'खत्म... टाटा... बाय-बाय!',
    r'आइए आपके इस अंतिम महा-निष्कर्ष को',
    r'चलो तुम्हारी इस .* थ्योरी को',
    r'ज़रा इस बात की गहराई और इस तीखे रोस्ट को महसूस कीजिए',
    r'बिल्कुल सही कहा आपने',
    r'अब एकदम सीधे और साफ शब्दों में बात करते हैं',
    r'जैसे दो भाई बैठकर आपस में दिल की बात करते हैं'
]

# Curated List of 100% Pure Hardcore Science Master Insights & Headlines
CURATED_PURE_SCIENCE_TOPICS = [
    {
        "headline": "दिमाग 3D दुनिया कैसे रेंडर करता है? 🧠",
        "tag": "NEUROSCIENCE & REALITY",
        "script": "क्या आप जानते हैं कि आपकी आँखें असल में कुछ नहीं देखतीं? न्यूरोसाइंस और क्वांटम फिजिक्स के अनुसार—बाहर की दुनिया में कोई रंग या ठोस वस्तु मौजूद नहीं है, सिर्फ इलेक्ट्रोमैग्नेटिक सिग्नल्स हैं! आपकी आँखें केवल उन सिग्नल्स को इलेक्ट्रिकल डेटा में बदलती हैं, और खोपड़ी के अंधेरे में बैठा दिमाग उस डेटा को प्रोसेस करके 3D दुनिया रेंडर करता है।"
    },
    {
        "headline": "परमाणु 99.9% खाली क्यों है? ⚛️",
        "tag": "QUANTUM PHYSICS & MATTER",
        "script": "अगर आप किसी परमाणु के न्यूक्लियस को फुटबॉल के आकार का मान लें, तो उसके चक्कर लगाने वाले इलेक्ट्रॉन दो किलोमीटर दूर होंगे! यानी जिसे हम ठोस दुनिया कहते हैं, वह 99.9999% खाली जगह है। फिर भी आप किसी दीवार के आर-पार क्यों नहीं जा पाते? क्योंकि इलेक्ट्रॉनों का इलेक्ट्रोस्टैटिक रिपल्शन आपको रोकता है!"
    },
    {
        "headline": "भविष्य पहले से लिखा है? ⏳",
        "tag": "BLOCK UNIVERSE & EINSTEIN",
        "script": "अल्बर्ट आइंस्टीन की थ्योरी ऑफ रिलेटिविटी के अनुसार, समय कोई बहती हुई नदी नहीं है। ब्रह्मांड एक 'ब्लॉक यूनिवर्स' है—जहाँ आपका भूतकाल, वर्तमान और भविष्य तीनों एक साथ पहले से ही जमे हुए बर्फ की तरह मौजूद हैं। हम सिर्फ चेतना के जरिए समय के एक-एक फ्रेम से होकर गुजर रहे हैं।"
    },
    {
        "headline": "क्वांटम ऑब्जर्वर इफेक्ट का सच 👁️",
        "tag": "DOUBLE SLIT EXPERIMENT",
        "script": "क्वांटम फिजिक्स का डबल-स्लिट एक्सपेरिमेंट साबित करता है कि जब तक कोई इलेक्ट्रॉन को देख नहीं रहा होता, वह एक साथ कई संभावनाओं की लहर (Wave) बनकर रहता है। लेकिन जैसे ही कोई चेतना उसे देखती है, वह तुरंत एक ठोस पार्टिकल में बदल जाता है! यानी वास्तविकता को बनने के लिए एक दृष्टा यानी ऑब्जर्वर की जरूरत होती है।"
    },
    {
        "headline": "दिमाग एक बायो-एंटीना है? 📡",
        "tag": "NEURAL FREQUENCIES",
        "script": "हमारा दिमाग विचार पैदा नहीं करता, बल्कि वह एक रेडियो रिसीवर की तरह काम करता है। जिस तरह रेडियो अलग-अलग फ्रीक्वेंसी ट्यून करके गाने पकड़ता है, ठीक उसी तरह हमारा न्यूरल नेटवर्क चेतना की कॉस्मिक फ्रीक्वेंसी से डेटा डाउनलोड करता है। जब आप अपनी ब्रेनवेव्स को अल्फा स्टेट में लाते हैं, तो इंट्यूशन अनलॉक होता है।"
    }
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
        Picks 100% Pure Hardcore Science scripts with professional high-retention headlines.
        """
        # Pick from curated pure science library first, with rotating index
        idx = len(self.used_scripts) % len(CURATED_PURE_SCIENCE_TOPICS)
        chosen = CURATED_PURE_SCIENCE_TOPICS[idx]
        self._save_history(f"curated_science_{idx}")

        return {
            "source_file": f"Pure_Science_Vol_{idx+1}",
            "narration": chosen["script"],
            "top_hook": chosen["headline"],
            "topic_tag": chosen["tag"]
        }

if __name__ == "__main__":
    engine = CosmicScriptEngine()
    data = engine.get_next_pro_script()
    print("Top Hook:", data["top_hook"])
    print("Topic Tag:", data["topic_tag"])
    print("Narration:", data["narration"])
