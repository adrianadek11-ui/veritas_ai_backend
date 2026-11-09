from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from core.brain import brain
from core.cache import cache
import asyncio
import json

app = FastAPI(title="Veritas AI Backend", version="1.3.0")

# Stały token korporacyjny NDA (w środowisku produkcyjnym pobierany ze zmiennych środowiskowych)
BEARER_TOKEN = "veritas-secret-secure-token-f1"

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.scheme != "Bearer" or credentials.credentials != BEARER_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"WebSocket client connected. Active connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print(f"WebSocket client disconnected. Active connections: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Broadcast error on connection: {e}")

manager = ConnectionManager()

class QueryRequest(BaseModel):
    query: str

@app.get("/")
async def root():
    return {"system": "Veritas AI Backend", "status": "ONLINE", "telemetry": "ACTIVE", "security": "ENABLED"}

@app.get("/metrics")
async def metrics_endpoint(token: str = Depends(verify_token)):
    return {
        "cache_stats": cache.get_stats(),
        "active_ws_connections": len(manager.active_connections),
        "system_status": "OPERATIONAL"
    }

@app.post("/query")
async def query_endpoint(payload: QueryRequest, token: str = Depends(verify_token)):
    result = await brain.route_and_process(payload.query)
    await manager.broadcast({"event": "NEW_QUERY_PROCESSED", "data": result})
    return result

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Opcjonalna autoryzacja tokena przekazywanego w subprotocol lub query param dla WebSocket
    token = websocket.query_params.get("token")
    if token != BEARER_TOKEN:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        print("WebSocket connection rejected: Invalid token.")
        return

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            result = await brain.route_and_process(data)
            await websocket.send_json({"event": "DIRECT_RESPONSE", "data": result})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)
        try:
            await websocket.close()
        except:
            pass
