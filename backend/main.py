from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.url_routes import router

# App banao
app = FastAPI(
    title="URL Shortener API",
    description="React + FastAPI + MongoDB URL Shortener",
    version="1.0.0"
)

# CORS — React (port 5173) ko Python backend (port 8000) se baat karne deta hai
# Bina CORS ke browser block kar deta hai requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "https://iurl.netlify.app",
],
    allow_credentials=True,
    allow_methods=["*"],   # GET, POST, sab allow
    allow_headers=["*"],
)

# Routes include karo
app.include_router(router)

# Root check — confirm karo server chal raha hai
@app.get("/health")
async def health_check():
    return {"status": "running", "message": "URL Shortener API is live!"}