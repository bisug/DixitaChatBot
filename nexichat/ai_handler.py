"""
AI Handler with Indian Attitude 😎
"""
from transformers import pipeline
import random

# Indian gaali responses 😂
GAALI_RESPONSES = {
    "bsdk": [
        "Abe ja na bsdk, tere se baat nahi karni 😂",
        "Tu khud dekh apne aap ko pehle 🤣",
        "Bsdk bol raha hai, aaine mein dekha hai kabhi? 💀",
        "Chal chal, apni maa ko ja bolna ye sab 😤",
        "Tera baap hu main, seedha bol 😎"
    ],
    "mc": [
        "Tameez se bol bhai, nahi to block kar dunga 🚫",
        "Gaali dega to gaali hi milegi, teri... 😤",
        "Bhai sahab, thoda manners seekh lo 🙄",
        "MC bol raha hai, khud ka dekh pehle 💀",
        "Teri maa ko puch kis se seekha ye sab 😂"
    ],
    "bc": [
        "BC bol ke cool ban gaya? Grow up bro 🤦",
        "Behen hai teri, nahi hai meri 😤",
        "Thik hai bhai, chill maar 😎",
        "BC bolna band kar, aur kuch baat kar 🙄",
        "Teri behen ko bol ye sab, mujhe mat bol 💀"
    ],
    "chutiya": [
        "Chutiya tu hai jo mujhse baat kar raha 😂",
        "Aaine mein dekh, pata chal jayega kaun chutiya hai 🤣",
        "Chal bhai, bura mat maan 😎",
        "Chutiya bolne se pehle soch le 🙄",
        "Thanks bhai, tu bhi 😂"
    ],
    "gandu": [
        "Gandu tu hai, main to AI hu 🤖",
        "Teri shakl dekh ke pata chal gaya kaun hai 😂",
        "Chill maar yaar, gussa kyu ho raha 😎",
        "Gandu bolne se kuch nahi hoga 🤦",
        "Okay bhai, tu bhi 💀"
    ],
    "madarchod": [
        "Respect bro, maa-baap ko respect kar 🙏",
        "Tameez nahi hai kya? Block kar dunga 🚫",
        "Teri maa ko bol ye sab, idhar mat bol 😤",
        "Bhai thoda decent ban, life mein kaam aayega 💯",
        "Chal hatt bsdk 😂"
    ],
    "bhosdk": [
        "Bhosdk bol ke bada cool ban gaya? 😂",
        "Tu khud dekh apni shakal 🤣",
        "Chal bhai, baat kar normal 😎",
        "Gaali dena band kar yaar 🙄",
        "Okay bro, peace ✌️"
    ],
    "lund": [
        "Scientific interest hai ya kya? 😂",
        "Biology class join kar le bhai 🤣",
        "Mature ban zara 🙄",
        "Kya baat kar raha hai yaar 😅",
        "Okay anatomy expert 💀"
    ]
}

# Casual gaali keywords
GAALI_KEYWORDS = [
    "bsdk", "bc", "mc", "chutiya", "gandu", "madarchod", 
    "bhosdk", "lund", "laude", "bhosdike", "chod", "gand",
    "lodu", "harami", "kamina", "kutta", "kutte", "saala",
    "randi", "behenchod", "maderchod"
]

class AIHandler:
    def __init__(self):
        self.model = None
        self.loaded = False
    
    def load_model(self):
        """Load Blenderbot model (lazy loading)"""
        if not self.loaded:
            try:
                print("Loading AI model...")
                self.model = pipeline(
                    "conversational",
                    model="facebook/blenderbot-400M-distill",
                    device=-1  # CPU
                )
                self.loaded = True
                print("✅ AI model loaded!")
            except Exception as e:
                print(f"❌ AI model load failed: {e}")
                self.loaded = False
    
    def is_gaali(self, text):
        """Check if message contains gaali"""
        text_lower = text.lower()
        for keyword in GAALI_KEYWORDS:
            if keyword in text_lower:
                return keyword
        return None
    
    def get_gaali_response(self, keyword):
        """Get savage response for gaali"""
        # Find matching gaali type
        for gaali_type, responses in GAALI_RESPONSES.items():
            if gaali_type in keyword:
                return random.choice(responses)
        
        # Generic savage response
        generic = [
            "Bhai tameez se baat kar, AI hu but insult bardaasht nahi karunga 😤",
            "Gaali dega to block kar dunga 🚫",
            "Cool ban raha hai kya? Grow up bro 🙄",
            "Respect do to respect milegi 💯",
            "Chal hatt, tere se baat nahi karni 😂"
        ]
        return random.choice(generic)
    
    def generate_response(self, message):
        """Generate AI response with attitude"""
        # Check for gaali first
        gaali = self.is_gaali(message)
        if gaali:
            return self.get_gaali_response(gaali)
        
        # Load model if not loaded
        if not self.loaded:
            self.load_model()
        
        # If model failed to load, return basic response
        if not self.loaded:
            return "Bhai thoda wait kar, main soch raha hu... 🤔"
        
        try:
            # Generate response from AI
            response = self.model(message)
            ai_reply = response[-1]['generated_text']
            
            # Add some Indian flavor randomly
            flavors = ["", " yaar", " bhai", " bro", " dude", " boss"]
            emojis = ["", " 😊", " 😎", " 👍", " 🔥", " ✨"]
            
            if random.random() < 0.3:  # 30% chance
                ai_reply += random.choice(flavors)
            
            if random.random() < 0.2:  # 20% chance
                ai_reply += random.choice(emojis)
            
            return ai_reply
            
        except Exception as e:
            print(f"AI error: {e}")
            return "Sorry bhai, thoda dimag kharab ho gaya... fir se bol? 😅"

# Global instance
ai_handler = AIHandler()
