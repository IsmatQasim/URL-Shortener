from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# .env file se settings load karo
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "urlshortener")

# MongoDB client — yeh ek baar banta hai, poori app use karti hai
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# urls collection — yahan sari URLs save hongi
url_collection = db["urls"]