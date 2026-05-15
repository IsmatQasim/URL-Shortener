from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

# Yeh model check karta hai ke user ne sahi data bheja ya nahi
class URLCreate(BaseModel):
    url: HttpUrl                        # Sirf valid URLs allow hoti hain
    custom_alias: Optional[str] = None  # User apna alias de sakta hai (optional)

# Yeh response mein wapas bhejte hain user ko
class URLResponse(BaseModel):
    short_url: str       # Jaise: http://localhost:8000/ab12Cd
    original_url: str    # Original long URL
    short_id: str        # Sirf ID: ab12Cd
    clicks: int = 0      # Kitni baar use hua
    created_at: datetime # Kab banaya