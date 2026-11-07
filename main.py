import os
import logging
import asyncio
from typing import Dict, Any, Optional, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from core.brain import brain
from core.stream_watcher import stream_watcher

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] VeritasF1: %(message)s")
logger = logging.getLogger("VeritasF1")

app = FastAPI(title="Veritas Matrix Nano-Core Enterprise Real-Time", version="62.0.0-PROD")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class UnifiedVerifyRequest(BaseModel):
    query: str = Field(..., min_length=1)
    context_data: Optional[Dict[str, Any]] = None

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
            logger.info("Klient WebSocket rozłączony.")

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Błąd transmisji WS: {e}")

manager = ConnectionManager()

os.makedirs("static", exist_ok=True)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(stream_watcher.start_background_monitoring())
    logger.info("Wszystkie jądra serwerowe Veritas F1 uruchomione pomyślnie.")

@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")

@app.get("/rezyserka")
async def serve_rezyserka():
    return FileResponse("static/index.html")

@app.get("/prowadzacy")
async def serve_prowadzacy():
    return FileResponse("static/index.html")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/api/verify")
async def verify_statement(req: UnifiedVerifyRequest) -> Dict[str, Any]:
    raw_query = req.query.strip()
    logger.info(f"Przetwarzanie tezy w rdzeniu głównym: '{raw_query}'")
    
    result = await brain.route_and_process(raw_query, req.context_data)
    return {
        "status": "SUCCESS",
        "query_corrected": raw_query,
        "direct_answer": result["direct_answer"],
        "sources": result["sources"],
        "anchor_munition": result["anchor_munition"],
        "disinformation_score": result["disinformation_score"]
    }

@app.post("/api/broadcast")
async def broadcast_action(data: dict):
    await manager.broadcast({"action": "UPDATE_STUDIO", "data": data})
    return {"status": "BROADCASTED"}

@app.post("/api/clear")
async def clear_system():
    await manager.broadcast({"action": "CLEAR"})
    return {"status": "CLEARED"}
