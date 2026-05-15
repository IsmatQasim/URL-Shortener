from nanoid import generate
from datetime import datetime, timedelta
from database.connection import url_collection
import os

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

# Short ID generate karna — sirf letters aur numbers (URL-safe)
def generate_short_id(size: int = 6) -> str:
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return generate(alphabet, size)

# Naya short URL banana
async def create_short_url(original_url: str, custom_alias: str = None):
    
    # Agar user ne custom alias diya hai toh use karo
    if custom_alias:
        # Check karo ke yeh alias pehle se exist toh nahi karta
        existing = await url_collection.find_one({"short_id": custom_alias})
        if existing:
            raise ValueError(f"'{custom_alias}' already exists. Choose another alias.")
        short_id = custom_alias
    else:
        # Nayi random ID generate karo
        # Collision handling: agar ID pehle se hai toh nayi banao
        short_id = generate_short_id()
        while await url_collection.find_one({"short_id": short_id}):
            short_id = generate_short_id()  # Repeat karo jab tak unique na mile

    # Database mein save karo
    url_doc = {
        "short_id": short_id,
        "original_url": original_url,
        "clicks": 0,
        "created_at": datetime.utcnow(),
        "expires_at": datetime.utcnow() + timedelta(days=7),  # 7 din baad expire
    }
    
    await url_collection.insert_one(url_doc)
    
    return {
        "short_id": short_id,
        "short_url": f"{BASE_URL}/{short_id}",
        "original_url": original_url,
        "clicks": 0,
        "created_at": url_doc["created_at"],
    }

# Short ID se original URL dhundhna
async def get_original_url(short_id: str):
    url_doc = await url_collection.find_one({"short_id": short_id})
    
    if not url_doc:
        return None  # ID exist nahi karti
    
    # Check karo ke expire toh nahi hua
    if url_doc.get("expires_at") and datetime.utcnow() > url_doc["expires_at"]:
        return None  # Expired hai
    
    # Click count badhao (analytics ke liye)
    await url_collection.update_one(
        {"short_id": short_id},
        {"$inc": {"clicks": 1}}  # clicks = clicks + 1
    )
    
    return url_doc["original_url"]