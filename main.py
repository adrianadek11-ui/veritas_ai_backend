import os
import json
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any

from core.brain import brain
from core.compliance_vault import ComplianceVault

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger("VeritasF1Master")

app = FastAPI(title="Veritas Matrix Nano-Core", version="64.0-F1 Thermal")

app.mount("/static", StaticFiles(directory="static"), name="static")

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Klient WebSocket połączony. Aktywnych: {len(self.active_connections)}")

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
    context: Optional[Dict[str, Any]] = None

class NanoSkinIngest(BaseModel):
    sensor_id: str
    cortisol_level: float
    gdr_value: float

@app.on_event("startup")
async def startup_event():
    logger.info("VeritasF1: Wszystkie jądra serwerowe (w tym Thermal Biometrics & Nano-Skin Protocol) uruchomione pomyślnie.")

@app.get("/")
async def get_index():
    return FileResponse("static/index.html")

@app.post("/api/verify")
async def api_verify(req: VerifyRequest):
    result = await brain.route_and_process(req.query, req.context)
    return result

@app.post("/api/broadcast")
async def api_broadcast(data: Dict[str, Any]):
    await manager.broadcast({"action": "UPDATE_STUDIO", "data": data})
    return {"status": "broadcasted"}

@app.post("/api/nano-skin/ingest")
async def api_nano_skin_ingest(payload: NanoSkinIngest):
    logger.info(f"Odebrano telemetrię z nano-skóry [{payload.sensor_id}]: Kortyzol={payload.cortisol_level}, GDR={payload.gdr_value}")
    await manager.broadcast({"action": "NANO_SKIN_UPDATE", "data": payload.dict()})
    return {"status": "ingested", "protocol": "v64.0-NANO-READY"}

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
