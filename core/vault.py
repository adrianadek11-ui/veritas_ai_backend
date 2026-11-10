import hashlib
import json
import os
import redis
from datetime import datetime
from core.post_quantum import pq_shield

class ComplianceVault:
    def __init__(self):
        redis_url = os.getenv("REDIS_URL", "redis://veritas_redis_cache:6379")
        try:
            self.client = redis.Redis.from_url(redis_url, decode_responses=True)
            self.client.ping()
            print("ComplianceVault connected to Redis successfully.")
        except Exception as e:
            print(f"ComplianceVault Redis connection warning: {e}")
            self.client = None

    def record_audit_trail(self, query: str, response_data: dict) -> dict:
        timestamp = datetime.utcnow().isoformat()
        raw_data = f"{timestamp}:{query}:{json.dumps(response_data, sort_keys=True)}"
        signature = hashlib.sha256(raw_data.encode("utf-8")).hexdigest()

        # Generowanie hybrydowego podpisu post-kwantowego
        pq_protection = pq_shield.encapsulate_signature(signature)

        audit_entry = {
            "timestamp": timestamp,
            "query": query,
            "signature": signature,
            "post_quantum_shield": pq_protection,
            "classification": response_data.get("nda_governance", {}).get("confidentiality_level", "STRICT_NDA_PROTECTED")
        }

        if self.client:
            try:
                self.client.lpush("veritas:audit:vault", json.dumps(audit_entry))
            except Exception as e:
                print(f"ComplianceVault Redis write error: {e}")

        return {
            "sha256_signature": signature,
            "post_quantum": pq_protection
        }

vault = ComplianceVault()
