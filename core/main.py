import logging
from fastapi import FastAPI, HTTPException

from fastapi.staticfiles import StaticFiles

# --- MONTOWANIE KATALOGU STATYCZNEGOKOKPITU ---
app.mount("/static", StaticFiles(directory="static"), name="static")

from pydantic import BaseModel
from typing import Dict, Any

# Konfiguracja logowania systemowego
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
log = logging.getLogger("VeritasGlobalF1")

app = FastAPI(
    title="Veritas Autonomous C2 System",
    version="2.1.0",
    description="Autonomiczny system dowodzenia z Okiem Prawdy, Tarczą Epistemiczną i Rejestrem Komend"
)

log.info("[*] Uruchamianie silników Veritas IE & Master Command Ecosystem...")

# Import modułów wewnętrznych systemu
try:
    from core.evolution_shield import evolution_shield
    from core.data_feeder import feeder
    from core.compliance_vault import vault, nda_engine
    from core.crypto_sentinel import crypto_sentinel
    from core.command_engine import command_engine
    log.info("[+] Wszystkie podsystemy, roje i silnik komend załadowane pomyślnie.")
except ImportError as e:
    log.warning(f"[!] Ostrzeżenie modułowe: {e}")

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
def read_root():
    return {
        "system": "Veritas Perpetuum Mobile C2",
        "status": "OPERATIONAL",
        "modules": [
            "Debate Buffer",
            "Rozwedka-Swarm",
            "Evolution Shield & Sandbox",
            "Data Feeder",
            "Compliance Vault & SHA-256",
            "Isolated Crypto-Sentinel",
            "Dynamic Voice/Text Command Engine"
        ]
    }

@app.post("/api/ingest")
def ingest_data(data: IngestRequest):
    result = feeder.process_incoming_nutrient(data.payload)
    return {"status": "SUCCESS", "feeder_response": result}

@app.post("/api/crypto/evaluate")
def evaluate_crypto(data: CryptoEvalRequest):
    evaluation = crypto_sentinel.evaluate_market_opportunity(data.asset, data.proposed_capital)
    cert = vault.record_verification(target=f"CRYPTO_TARGET_{data.asset}", client_id="OPERATOR_VIP")
    return {
        "status": "EVALUATED_BY_CRYPTO_SWARM",
        "evaluation": evaluation,
        "compliance_certificate": cert["certificate_sha256"]
    }

@app.post("/api/command/execute")
def execute_cmd(data: CommandRequest):
    """Przyjmuje komendę z panelu lub asystenta głosowego i wykonuje ją."""
    res = command_engine.execute_command(data.command)
    return res

@app.post("/api/command/register")
def register_cmd(data: RegisterCommandRequest):
    """Pozwala operatorowi dodać nową komendę do słownika systemu w locie."""
    res = command_engine.register_command(data.command_name, data.description)
    return res
