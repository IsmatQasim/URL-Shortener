from datetime import datetime, timedelta
from database.connection import url_collection
from utils.base62 import url_to_short_id  
import os

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


async def create_short_url(original_url: str, custom_alias: str = None):
    """
    Main function — long URL lo, short ID banao, DB mein save karo
    """

    # --- Custom Alias Case ---
    if custom_alias:
        existing = await url_collection.find_one({"short_id": custom_alias})
        if existing:
            raise ValueError(f"'{custom_alias}' already taken. Choose another.")
        short_id = custom_alias

    else:
        # --- Base62 + Collision Handling ---
        #
        # attempt=0: MD5 hash ke pehle 8 hex chars use karo
        # attempt=1: agley 8 chars (agar collision hua)
        # attempt=2: aur agley...

        max_attempts = 5
        short_id = None

        for attempt in range(max_attempts):
            candidate = url_to_short_id(original_url, attempt)
            existing = await url_collection.find_one({"short_id": candidate})

            if not existing:
                short_id = candidate
                break

        if not short_id:
            raise Exception("Could not generate unique ID. Try again.")

    # --- Database mein save karo ---
    url_doc = {
        "short_id": short_id,
        "original_url": original_url,
        "clicks": 0,
        "created_at": datetime.utcnow(),
        "expires_at": datetime.utcnow() + timedelta(days=7),
    }

    await url_collection.insert_one(url_doc)

    return {
        "short_id": short_id,
        "short_url": f"{BASE_URL}/{short_id}",
        "original_url": original_url,
        "clicks": 0,
        "created_at": url_doc["created_at"],
    }


async def get_original_url(short_id: str):
    url_doc = await url_collection.find_one({"short_id": short_id})

    if not url_doc:
        return None

    if url_doc.get("expires_at") and datetime.utcnow() > url_doc["expires_at"]:
        return None

    await url_collection.update_one(
        {"short_id": short_id},
        {"$inc": {"clicks": 1}}
    )

    return url_doc["original_url"]


async def get_url_stats(short_id: str):
    url_doc = await url_collection.find_one({"short_id": short_id})

    if not url_doc:
        return None

    return {
        "short_id": short_id,
        "original_url": url_doc["original_url"],
        "clicks": url_doc["clicks"],
        "created_at": url_doc["created_at"],
        "expires_at": url_doc["expires_at"],
    }