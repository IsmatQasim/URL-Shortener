from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from models.url_model import URLCreate, URLResponse
from services.url_service import create_short_url, get_original_url, get_all_urls, get_url_stats

router = APIRouter()

@router.post("/api/shorten", response_model=URLResponse)
async def shorten_url(data: URLCreate, request: Request):
    try:
        client_id = request.headers.get("X-Client-Id") or request.client.host
        result = await create_short_url(
            original_url=str(data.url),
            custom_alias=data.custom_alias,
            created_by=client_id
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error. Try again.")

@router.get("/api/urls")
async def get_urls(request: Request):
    client_id = request.headers.get("X-Client-Id") or request.client.host
    urls = await get_all_urls(client_id)
    return urls

@router.get("/api/stats/{short_id}")
async def url_stats(short_id: str):
    stats = await get_url_stats(short_id)
    if not stats:
        raise HTTPException(status_code=404, detail="URL not found.")
    return stats

# ← Naya route — frontend redirect ke liye
@router.get("/api/resolve/{short_id}")
async def resolve_url(short_id: str):
    original_url = await get_original_url(short_id)
    if not original_url:
        raise HTTPException(status_code=404, detail="URL not found or expired.")
    return {"original_url": original_url}

# Yeh SABSE NEECHE rehna chahiye
@router.get("/{short_id}")
async def redirect_url(short_id: str):
    original_url = await get_original_url(short_id)
    if not original_url:
        raise HTTPException(status_code=404, detail="URL not found or expired.")
    return RedirectResponse(url=original_url, status_code=307)