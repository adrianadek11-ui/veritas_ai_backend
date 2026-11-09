from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from core.brain import brain
from core.cache import cache
from core.clips import clips_generator
from core.biometrics import biometrics_engine
from core.dispatcher import dispatcher
from core.reporter import compliance_reporter
import asyncio
import json

app = FastAPI(title="Veritas AI Backend", version="1.7.0")

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

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Broadcast error: {e}")

manager = ConnectionManager()

class QueryRequest(BaseModel):
    query: str

@app.get("/")
async def root():
    return {"system": "Veritas AI Backend", "status": "ONLINE", "compliance_reporter": "ACTIVE"}

@app.get("/metrics")
async def metrics_endpoint(token: str = Depends(verify_token)):
    return {
        "cache_stats": cache.get_stats(),
        "active_ws_connections": len(manager.active_connections),
        "system_status": "OPERATIONAL"
    }

@app.get("/report/compliance")
async def compliance_report_endpoint(token: str = Depends(verify_token)):
    return compliance_reporter.generate_audit_report()

@app.post("/query")
async def query_endpoint(payload: QueryRequest, token: str = Depends(verify_token)):
    result = await brain.route_and_process(payload.query)
    result["advanced_voice_biometrics"] = biometrics_engine.analyze_speaker(payload.query)
    
    dispatch_log = await dispatcher.dispatch_alert("NEW_QUERY_EVALUATED", {
        "query": payload.query,
        "disinformation_score": result.get("disinformation_score"),
        "swarm_consensus": result.get("swarm_consensus"),
        "advanced_voice_biometrics": result.get("advanced_voice_biometrics")
    })
    result["mcr_dispatch_status"] = dispatch_log

    await manager.broadcast({"event": "NEW_QUERY_PROCESSED", "data": result})
    return result

@app.post("/clips")
async def clips_endpoint(payload: QueryRequest, token: str = Depends(verify_token)):
    result = await brain.route_and_process(payload.query)
    viral_package = clips_generator.generate_viral_clip_package(payload.query, result)
    return viral_package

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if token != BEARER_TOKEN:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            result = await brain.route_and_process(data)
            result["advanced_voice_biometrics"] = biometrics_engine.analyze_speaker(data)
            await websocket.send_json({"event": "DIRECT_RESPONSE", "data": result})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        manager.disconnect(websocket)
        try:
            await websocket.close()
        except:
            pass
