import random
from typing import Dict

# Preset viral templates for quick generation without external AI API
VIRAL_TEMPLATES = {
    "gta6_leaks": [
        {
            "hook": "GTA 6 ke bare me ye 3 secret leaks aapko kisi ne nahi bataye!",
            "points": [
                "Pehla leak, Vice City ka map GTA 5 se do guna bada hoga aur lagbhag 70% buildings enter karne layak hongi.",
                "Doosra leak, GTA 6 me AI NPCs itne smart honge ki wo aapke kapde aur driving style par react karenge.",
                "Teesra leak, dynamic weather system jo sach me hurricanes aur floods create karega!"
            ],
            "cta": "Aap GTA 6 ke liye kitne excited ho? Comment karke batao aur follow karna mat bhoolna!"
        },
        {
            "hook": "Rockstar Games is hiding this massive GTA 6 feature from everyone!",
            "points": [
                "Number one: The police system is completely revamped with memory tracking for crimes.",
                "Number two: Realistic weapon carrying limit, just like Red Dead Redemption 2.",
                "Number three: Over seven hundred enterable buildings across Vice City and beyond."
            ],
            "cta": "Are you buying GTA 6 on day one? Drop your thoughts below and subscribe for more!"
        },
        {
            "hook": "GTA 6 ka pricing dekh kar sabke hosh udne wale hain!",
            "points": [
                "Reports ke mutabiq, GTA 6 ka standard edition normal games se mehenga ho sakta hai.",
                "Kaha ja raha hai ki Rockstar ne is game par 2 billion dollars se jyada invest kiya hai.",
                "Isliye graphic quality aur storyline bilkul next-level hone wali hai."
            ],
            "cta": "Kya aap iske liye 70 dollar se jyada dene ko tayyar hain? Comment me batayein!"
        }
    ],
    "gaming_facts": [
        {
            "hook": "Top 3 insane gaming facts that sound completely fake!",
            "points": [
                "Fact one: GTA 5 made 1 billion dollars in just 3 days of release.",
                "Fact two: Minecraft world is technically bigger than the surface of Neptune.",
                "Fact three: Mario was originally named Jumpman and he was a carpenter, not a plumber."
            ],
            "cta": "Which fact surprised you the most? Subscribe for more daily gaming facts!"
        }
    ]
}


class ScriptGenerator:
    def __init__(self):
        pass

    def generate_script(self, category: str = "gta6_leaks", language: str = "hi") -> Dict[str, str]:
        """
        Generates a viral short script, title, description, and tags.
        """
        templates = VIRAL_TEMPLATES.get(category, VIRAL_TEMPLATES["gta6_leaks"])
        selected = random.choice(templates)
        
        # Build narration script
        narration_text = f"{selected['hook']} {' '.join(selected['points'])} {selected['cta']}"
        
        # Titles and tags
        if "GTA 6" in selected['hook']:
            title = "GTA 6 Insane Secret Leaks! 🤯 #shorts #gta6 #gaming"
            tags = ["GTA 6", "GTA VI", "GTA 6 Leaks", "Rockstar Games", "GTA 6 Gameplay", "Shorts", "Gaming Shorts"]
        else:
            title = "Insane Gaming Facts You Won't Believe! 🎮 #shorts #gaming"
            tags = ["Gaming Facts", "Shorts", "Gaming", "Video Games", "Facts"]
            
        description = f"{selected['hook']}\n\n{narration_text}\n\n#shorts #gta6 #gaming #rockstargames #viral"
        
        return {
            "title": title,
            "script": narration_text,
            "description": description,
            "tags": tags,
            "category": category,
            "language": language
        }


if __name__ == "__main__":
    gen = ScriptGenerator()
    res = gen.generate_script("gta6_leaks")
    print("Generated Title:", res["title"])
    print("Generated Script:", res["script"])
