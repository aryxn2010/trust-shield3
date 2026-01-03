import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import config
from fastapi.staticfiles import StaticFiles
# =================================================================
# 🚨 CRITICAL WINDOWS FIX
# This sets the correct Event Loop policy BEFORE the app starts.
# =================================================================
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
# =================================================================

# Import routes AFTER setting the loop policy
from api_bundle import router as api_router
app = FastAPI(title="TrustShield AI API")
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api/v1")
@app.get("/")
def root():
    return {"status": "TrustShield System Online"}

if __name__ == "__main__":
    import uvicorn
    
    # Get the PORT from the environment (Render/Railway sets this automatically)
    # If not found (e.g., on your laptop), default to 8000
    port = int(os.environ.get("PORT", 8000))
    
    print(f"🚀 Starting TrustShield Server on Port {port}...")
    
    # 1. Pass 'app' directly (safer than string "backend.main:app")
    # 2. Set reload=False for production (saves memory/cpu)
    uvicorn.run(app, host="0.0.0.0", port=port)