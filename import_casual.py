from pymongo import MongoClient
import sys

MONGO_URL = "mongodb+srv://vclub:vclub@vclub.hauilrr.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGO_URL)
db = client["Word"]["WordDb"]

# Read casual chats
with open('/tmp/casual_human_chats.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

added = 0
skipped = 0

for line in lines:
    line = line.strip()
    if not line or '|' not in line:
        continue
    
    parts = line.split('|', 1)
    if len(parts) != 2:
        continue
    
    query = parts[0].strip().lower()
    response = parts[1].strip()
    
    # Check if already exists
    existing = db.find_one({"word": query})
    if existing:
        skipped += 1
        continue
    
    # Add to database
    db.insert_one({
        "word": query,
        "text": response,
        "check": "text",
        "source": "casual_human"
    })
    added += 1

print(f"✅ Added {added} new casual conversations")
print(f"⏭️ Skipped {skipped} duplicates")
print(f"📊 Total in DB: {db.count_documents({})}")
