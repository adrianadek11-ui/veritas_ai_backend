import os
import json
import logging
import random
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from core.brain import brain
from core.compliance_vault import ComplianceVault

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger("VeritasGlobalF1")

app = FastAPI(title="Veritas Matrix Nano-Core Global F1", version="66.0-ANALYTICS")

app.mount("/static", StaticFiles(directory="static"), name="static")

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Klient WebSocket połączony z Globalnym Centrum Analytics. Aktywnych: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"Klient WebSocket rozłączony. Aktywnych: {len(self.active_connections)}")

    async def broadcast(self, message: Dict[str, Any]):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Błąd transmisji WS: {e}")

manager = ConnectionManager()

class VerifyRequest(BaseModel):
    query: str
    source_feed: Optional[str] = "TVN24"
    context: Optional[Dict[str, Any]] = None

class NanoSkinIngest(BaseModel):
    sensor_id: str
    cortisol_level: float
    gdr_value: float

@app.on_event("startup")
async def startup_event():
    logger.info("VeritasF1 Analytics: Wszystkie jądra (Multi-Stream, IR Thermal, Safety Interlock, Reach Analytics) aktywne.")

@app.get("/")
async def get_index():
    return FileResponse("static/index.html")

@app.post("/api/verify")
async def api_verify(req: VerifyRequest):
    result = await brain.route_and_process(req.query, req.context)
    result["active_source_feed"] = req.source_feed
    
    # Symulacja i obliczanie wskaźników zasięgu dla nowo przetworzonej tezy
    score = result.get("disinformation_score", 35.0)
    safety_passed = score >= 40.0 or score <= 20.0
    
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
    return result

@app.post("/api/broadcast")
async def api_broadcast(data: Dict[str, Any]):
    await manager.broadcast({"action": "UPDATE_STUDIO", "data": data})
    return {"status": "broadcasted"}

@app.post("/api/nano-skin/ingest")
async def api_nano_skin_ingest(payload: NanoSkinIngest):
    logger.info(f"Odebrano telemetrię nano-skóry [{payload.sensor_id}]: Kortyzol={payload.cortisol_level}")
    await manager.broadcast({"action": "NANO_SKIN_UPDATE", "data": payload.dict()})
    return {"status": "ingested", "protocol": "v66.0-ANALYTICS-READY"}

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
