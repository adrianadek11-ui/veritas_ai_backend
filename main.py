import os, time, logging
from typing import Dict, Any, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from core.brain import brain

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] VeritasF1: %(message)s")
logger = logging.getLogger("VeritasF1")

app = FastAPI(title="Veritas Matrix Nano-Core Enterprise", version="52.0.0-PROD")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class UnifiedVerifyRequest(BaseModel):
    query: str = Field(..., min_length=1)
    context_data: Optional[Dict[str, Any]] = None

# Pobieranie kluczy ze zmiennych środowiskowych zamiast na sztywno w kodzie
GCP_API_KEY = os.getenv("GCP_API_KEY", "")

os.makedirs("static", exist_ok=True)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_frontend():
    frontend_path = "static/index.html"
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {"status": "ONLINE", "info": "Silnik Veritas gotowy."}

@app.post("/api/verify")
async def verify_statement(req: UnifiedVerifyRequest) -> Dict[str, Any]:
    query = req.query.strip()
    brain_response = await brain.route_and_process(query, req.context_data)
    
    return {
        "status": "SUCCESS",
        "direct_answer": brain_response["direct_answer"],
        "sources": brain_response["sources"],
        "anchor_munition": brain_response["anchor_munition"],
        "disinformation_score": brain_response["disinformation_score"]
    }
