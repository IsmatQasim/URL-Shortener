from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from models.url_model import URLCreate, URLResponse
from services.url_service import create_short_url, get_original_url, get_all_urls, get_url_stats

router = APIRouter()


# POST /api/shorten — naya short URL banao
@router.post("/api/shorten", response_model=URLResponse)
async def shorten_url(data: URLCreate, request: Request):
    try:
        # Client ka IP address nikalo
        # request.client.host → "192.168.1.1" jaisi value
        client_ip = request.client.host

        result = await create_short_url(
            original_url=str(data.url),
            custom_alias=data.custom_alias,
            created_by=client_ip        # IP save karo — taake pata chale kiska URL hai
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error. Try again.")


# GET /api/urls — sirf US USER ki URLs (IP se identify)
@router.get("/api/urls")
async def get_urls(request: Request):
    client_ip = request.client.host
    urls = await get_all_urls(client_ip)   # Sirf is IP ki URLs aayengi
    return urls


# GET /api/stats/{short_id} — kisi ek URL ki stats
@router.get("/api/stats/{short_id}")
async def url_stats(short_id: str):
    stats = await get_url_stats(short_id)
    if not stats:
        raise HTTPException(status_code=404, detail="URL not found.")
    return stats


# GET /{short_id} — redirect karo
# NOTE: Yeh SABSE NEECHE hona chahiye
# Warna /api/urls bhi short_id samajh leta hai FastAPI
@router.get("/{short_id}")
async def redirect_url(short_id: str):
    original_url = await get_original_url(short_id)
    if not original_url:
        raise HTTPException(status_code=404, detail="URL not found or expired.")
    return RedirectResponse(url=original_url, status_code=307)