import logging
import sys
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from core.brain import brain
from core.compliance_vault import ComplianceVault
from core.media_intelligence import media_intelligence

# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("VeritasF1Master")

app = FastAPI(title="Veritas Matrix Nano-Core - Media Edition F1", version="63.0-PROD")

# Montowanie plików statycznych (Frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

class QueryModel(BaseModel):
    query: str

class ClashModel(BaseModel):
    speaker: str
    target: str
    statement: str

# Stan połączeń WebSocket w czasie rzeczywistym
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

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Błąd broadcastu WebSocket: {e}")

manager = ConnectionManager()

@app.on_event("startup")
async def startup_event():
    logger.info("VeritasF1: Wszystkie jądra serwerowe (w tym Media Intelligence & Vault) uruchomione pomyślnie.")
    logger.info("VeritasF1: Globalny Nasłuch Strumieniowy i Analiza Sentymentu aktywne w tle.")

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/verify")
async def verify_statement(payload: QueryModel):
    """Główny endpoint weryfikacji tezy przez Live Web RAG."""
    result = await brain.route_and_process(payload.query)
    # Dodajemy analizę sentymentu społecznego do wyników
    sentiment = media_intelligence.compute_social_sentiment(payload.query)
    result["sentiment_data"] = sentiment
    return JSONResponse(content=result)

@app.post("/api/clash")
async def analyze_clash(payload: ClashModel):
    """Endpoint analizujący starcie między politykami (Prawo do repliki)."""
    clash_result = media_intelligence.analyze_debate_clash(payload.speaker, payload.target, payload.statement)
    return JSONResponse(content=clash_result)

@app.post("/api/broadcast")
async def broadcast_to_studio(payload: dict):
    """Rozgłasza wynik analizy do reżyserki, studia i chatbota przez WebSocket."""
    await manager.broadcast({
        "action": "UPDATE_STUDIO",
        "data": payload
    })
    return {"status": "ok", "broadcasted": True}

@app.post("/api/clear")
async def clear_system_state():
    """Resetuje stan systemowy i powiadamia wszystkie panele."""
    await manager.broadcast({"action": "CLEAR"})
    return {"status": "reset_ok"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Odebrano komunikat przez WS: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
