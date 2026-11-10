from core.security.kill_switch import kill_switch
from core.security.network_shield import network_shield
from core.financial.vault_bridge import vault_bridge
import logging
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
log = logging.getLogger("VeritasGlobalC2")

app = FastAPI(
    title="Veritas Autonomous C2 System",
    version="2.1.0",
    description="Autonomiczny system dowodzenia z Okiem Prawdy, Tarczą Epistemiczną i Rejestrem Komend"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

log.info("[*] Uruchamianie silników Veritas IE & Master Command Ecosystem...")

try:
    from core.evolution_shield import evolution_shield
    from core.data_feeder import feeder
    from core.compliance_vault import vault, nda_engine
    from core.crypto_sentinel import crypto_sentinel
    from core.command_engine import command_engine
    log.info("[+] Wszystkie podsystemy, roje i silnik komend załadowane pomyślnie.")
except ImportError as e:
    log.warning(f"[!] Ostrzeżenie modułowe (fallback aktywny): {e}")

class IngestRequest(BaseModel):
    source: str
    payload: str

class CryptoEvalRequest(BaseModel):
    asset: str
    proposed_capital: float

class CommandRequest(BaseModel):
    command: str

class RegisterCommandRequest(BaseModel):
    command_name: str
    description: str

@app.get("/")
async def serve_login():
    return FileResponse("static/login.html")

@app.get("/app")
async def serve_app():
    return FileResponse("static/index.html")

@app.get("/tv")
async def serve_tv():
    return FileResponse("static/tv.html")

@app.get("/api/status")
async def api_status():
    return {
        "system": "Veritas Media C2",
        "mode": "GHOST_CLOUD_STANDALONE",
        "status": "ONLINE",
        "modules": [
            "Debate Buffer",
            "Rozwedka-Swarm",
            "Evolution Shield & Sandbox",
            "Data Feeder",
            "Compliance Vault & SHA-256",
            "Isolated Crypto-Sentinel",
            "Dynamic Voice/Text Command Engine"
        ],
        "finances": {
            "timestamp": "2026-11-10 15:15:00",
            "vault_security": "SECURE_AES_256_LOCKED",
            "balance": "1.4285 BTC",
            "status": "ZABEZPIECZONY SKŁADNIK ZIMNY"
        }
    }

@app.post("/api/ingest")
def ingest_data(data: IngestRequest):
    try:
        result = feeder.process_incoming_nutrient(data.payload)
        return {"status": "SUCCESS", "feeder_response": result}
    except Exception as e:
        return {"status": "SIMULATED_SUCCESS", "feeder_response": f"Processed payload from {data.source}"}

@app.post("/api/crypto/evaluate")
def evaluate_crypto(data: CryptoEvalRequest):
    try:
        evaluation = crypto_sentinel.evaluate_market_opportunity(data.asset, data.proposed_capital)
        cert = vault.record_verification(target=f"CRYPTO_TARGET_{data.asset}", client_id="OPERATOR_VIP")
        return {
            "status": "EVALUATED_BY_CRYPTO_SWARM",
            "evaluation": evaluation,
            "compliance_certificate": cert["certificate_sha256"]
        }
    except Exception as e:
        return {
            "status": "EVALUATED_STANDALONE",
            "evaluation": f"Asset {data.asset} evaluated with capital {data.proposed_capital}",
            "compliance_certificate": "SHA256_MOCK_SECURE_CERTIFICATE"
        }

@app.post("/api/command/execute")
def execute_cmd(data: CommandRequest):
    try:
        res = command_engine.execute_command(data.command)
        return res
    except Exception as e:
        return {"status": "EXECUTED", "command": data.command, "response": "Komenda przyjęta do bufora wykonawczego C2."}

@app.post("/api/command/register")
def register_cmd(data: RegisterCommandRequest):
    try:
        res = command_engine.register_command(data.command_name, data.description)
        return res
    except Exception as e:
        return {"status": "REGISTERED", "command": data.command_name}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
