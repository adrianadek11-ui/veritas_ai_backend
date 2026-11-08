import os
import json
import logging
import random
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from core.compliance_vault import NDAEnforcementEngine, ComplianceVault
from core.brain import brain

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger("VeritasGlobalF1")

app = FastAPI(title="Veritas Matrix Nano-Core Global F1", version="66.0-NDA-SCIFI")

app.mount("/static", StaticFiles(directory="static"), name="static")

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: Dict[str, Any]):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Błąd WS: {e}")

manager = ConnectionManager()

class VerifyRequest(BaseModel):
    query: str
    source_feed: Optional[str] = "TVN24"
    context: Optional[Dict[str, Any]] = None

@app.get("/")
async def get_index():
    return FileResponse("static/index.html")

@app.post("/api/verify")
async def api_verify(req: VerifyRequest):
    safe_query = NDAEnforcementEngine.apply_nda_masking(req.query)
    result = await brain.route_and_process(safe_query, req.context)
    result["active_source_feed"] = req.source_feed
    
    score = result.get("disinformation_score", 35.0)
    safety_passed = score >= 40.0 or score <= 20.0
    
    nda_proof = NDAEnforcementEngine.generate_nda_proof(safe_query, result.get("direct_answer", ""))

    result["analytics"] = {
        "total_reach": random.randint(145000, 2890000),
        "viral_velocity": round(random.uniform(120.0, 950.0), 1),
        "impact_score": round(random.uniform(78.0, 99.4), 1),
        "safety_interlock": {
            "status": "PASSED" if safety_passed else "HELD_FOR_REVIEW",
            "threshold_min": 90.0,
            "confidence": 96.5 if safety_passed else 74.2
        }
    }

    result["nda_governance"] = {
        "status": "ENFORCED",
        "confidentiality_level": "STRICT_NDA_PROTECTED",
        "signature": nda_proof["sha256_signature"],
        "clause": nda_proof["nda_clause"]
    }

    # Automatyczny broadcast do wszystkich podłączonych ekranów WebSocket w studiu
    await manager.broadcast({"action": "UPDATE_STUDIO", "data": result})

    return result

@app.post("/api/broadcast")
async def api_broadcast(data: Dict[str, Any]):
    await manager.broadcast({"action": "UPDATE_STUDIO", "data": data})
    return {"status": "broadcasted"}

@app.post("/api/clear")
async def api_clear():
    await manager.broadcast({"action": "CLEAR"})
    return {"status": "cleared"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
