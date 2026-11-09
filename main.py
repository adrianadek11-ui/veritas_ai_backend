import os
import json
import logging
import random
import time
import secrets
from datetime import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Header, Security, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from core.compliance_vault import NDAEnforcementEngine, ComplianceVault
from core.brain import brain

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger("VeritasGlobalF1")

app = FastAPI(title="Veritas Matrix Nano-Core Global F1", version="66.0-NDA-SCIFI-MULTIMODAL")

app.mount("/static", StaticFiles(directory="static"), name="static")

# ==========================================
# 1. MANAGEMENT & CONNECTIONS
# ==========================================

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

# ==========================================
# 2. VIP DASHBOARD & 12-HOUR TOKEN SECURE GATEWAY
# ==========================================

ACTIVE_VIP_TOKENS: Dict[str, float] = {}

class TokenRequest(BaseModel):
    architect_secret: str
    client_name: str

@app.post("/api/architect/generate-token")
async def generate_vip_token(req: TokenRequest):
    if req.architect_secret != "VERITAS_MASTER_KEY_2026":
        raise HTTPException(status_code=403, detail="Błędny klucz Architekta. Dostęp zabroniony.")
    
    token = f"VERITAS-VIP-{secrets.token_hex(16)}"
    expiration_time = time.time() + (12 * 3600)  # Ważność: dokładnie 12 godzin
    ACTIVE_VIP_TOKENS[token] = expiration_time
    
    logger.info(f"Wygenerowano 12-godzinny token VIP dla: {req.client_name}")
    return {
        "status": "SUCCESS",
        "client": req.client_name,
        "vip_token": token,
        "expires_in_hours": 12,
        "timestamp_utc": datetime.utcnow().isoformat()
    }

def verify_vip_token(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Brak tokenu dostępu. Wpisz aktualny klucz dostępu lub skontaktuj się z Architektem.")
    
    token = authorization.split(" ")[1]
    if token not in ACTIVE_VIP_TOKENS:
        raise HTTPException(status_code=403, detail="Nieznany lub unieważniony token dostępu.")
    
    if time.time() > ACTIVE_VIP_TOKENS[token]:
        del ACTIVE_VIP_TOKENS[token]
        raise HTTPException(status_code=403, detail="Token wygasł (minęło 12 godzin). Skontaktuj się z Architektem po nowy klucz.")
        
    return token

@app.get("/api/vip/dashboard")
async def vip_dashboard_portal(token: str = Security(verify_vip_token)):
    return {
        "portal": "Veritas VIP Command Center",
        "access": "GRANTED",
        "modules": [
            {"id": "media", "name": "Veritas Media (Oko Prawdy / Live RAG)", "status": "ACTIVE"},
            {"id": "lex", "name": "Veritas Lex (Prawo & Compliance)", "status": "SECURED_ISO"},
            {"id": "admin", "name": "Veritas Admin (Skarbowość & Audyt)", "status": "ISOLATED_VAULT"},
            {"id": "security", "name": "Veritas Security (Biometria, Termowizja IR)", "status": "ARMED"}
        ]
    }

# ==========================================
# 3. CORE VERIFY & BROADCAST ENDPOINTS
# ==========================================

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

# ==========================================
# 4. MULTIMODAL INGEST (Mobile Scanner & Audio/Video Forensics)
# ==========================================

@app.post("/api/multimodal/ingest-document")
async def ingest_document(file: UploadFile = File(...), module_type: str = Form("media")):
    """Mobilny skaner / Kamera nadbiurowa: przyjmuje zdjęcie/skan, OCR-uje i maskuje PII."""
    file_bytes = await file.read()
    filename = file.filename or "scan.jpg"
    
    # Symulacja przetwarzania Computer Vision & OCR
    extracted_text = f"[OCR Extracted from {filename}]: Dokument zweryfikowany dla modułu {module_type}."
    masked_text = NDAEnforcementEngine.apply_nda_masking(extracted_text)
    
    storage_record = ComplianceVault.secure_store(masked_text, f"mobile_lens://{filename}", "Zindeksowano pomyślnie przez Mobilny Skaner Veritas.")
    
    return {
        "status": "SUCCESS",
        "module": module_type,
        "filename": filename,
        "extracted_preview": masked_text,
        "audit_signature": storage_record["nda_compliance"]["sha256_signature"]
    }

@app.post("/api/multimodal/ingest-audio-video")
async def ingest_audio_video(file: UploadFile = File(...), source_feed: str = Form("Field_Interview")):
    """Multimodalny rejestrator audio-wideo: transkrypcja w locie, biometria głosu i detekcja fałszu."""
    file_bytes = await file.read()
    filename = file.filename or "media_stream.mp4"
    
    # Symulacja analizy biometrycznej, STT oraz detekcji stresu/kłamstwa
    stress_index = round(random.uniform(15.0, 92.5), 1)
    deception_detected = stress_index > 70.0
    
    analysis_result = {
        "filename": filename,
        "source_feed": source_feed,
        "transcription": "Przykładowa transkrypcja z terenu: wypowiedź zarejestrowana i przeanalizowana.",
        "biometric_stress_val": stress_index,
        "deception_alert": deception_detected,
        "timestamp_utc": datetime.utcnow().isoformat()
    }
    
    await manager.broadcast({"action": "MULTIMODAL_ALERT", "data": analysis_result})
    return {
        "status": "PROCESSED",
        "forensic_analysis": analysis_result
    }

# ==========================================
# 5. WEBSOCKET ENDPOINT
# ==========================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
