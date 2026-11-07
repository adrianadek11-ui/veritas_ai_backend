import os
import json
import hashlib
from datetime import datetime

VAULT_DIR = "compliance_storage"
os.makedirs(VAULT_DIR, exist_ok=True)

class ComplianceVault:
    @staticmethod
    def secure_store(claim: str, source_url: str, content_snippet: str) -> str:
        timestamp = datetime.utcnow().isoformat()
        raw_data = f"{claim}|{source_url}|{content_snippet}|{timestamp}"
        sha_hash = hashlib.sha256(raw_data.encode('utf-8')).hexdigest()
        
        record = {
            "timestamp": timestamp,
            "claim": claim,
            "source_url": source_url,
            "content_snippet": content_snippet,
            "sha256": sha_hash,
            "status": "VERIFIED_TRUTH_ARCHIVE"
        }
        
        filename = os.path.join(VAULT_DIR, f"{sha_hash[:16]}.json")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
            
        return sha_hash
