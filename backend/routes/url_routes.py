from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from models.url_model import URLCreate, URLResponse
from services.url_service import create_short_url, get_original_url

router = APIRouter()

# POST /api/shorten — naya short URL banao
@router.post("/api/shorten", response_model=URLResponse)
async def shorten_url(data: URLCreate):
    try:
        result = await create_short_url(
            original_url=str(data.url),
            custom_alias=data.custom_alias
        )
        return result
    except ValueError as e:
        # Custom alias already exists
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error. Try again.")

# GET /{short_id} — redirect karo original URL pe
@router.get("/{short_id}")
async def redirect_url(short_id: str):
    original_url = await get_original_url(short_id)
    
    if not original_url:
        raise HTTPException(
            status_code=404,
            detail="URL not found or has expired."
        )
    
    # 307 = Temporary Redirect (browser original URL pe chala jaata hai)
    return RedirectResponse(url=original_url, status_code=307)