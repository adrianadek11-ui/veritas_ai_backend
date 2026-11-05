import os, json, logging
from datetime import datetime
from cryptography.fernet import Fernet

class ComplianceVault:
    def __init__(self, log_path="compliance_audit.log"):
        self.log_path = log_path
        key_env = os.getenv("VERITAS_VAULT_KEY")
        self.key = key_env.encode('utf-8') if key_env else b'G3F8fH1k93jD_lAqwX7zP_MnbvCxZlkjhgfdsaQWER4=' 
        self.cipher = Fernet(self.key)

    def log_action(self, query: str, answer: str, status: str) -> str:
        payload = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "query": query, "answer": answer, "status": status}
        json_data = json.dumps(payload).encode('utf-8')
        encrypted_data = self.cipher.encrypt(json_data)
        with open(self.log_path, "ab") as log_file:
            log_file.write(encrypted_data + b'\n')
        return encrypted_data.decode('utf-8')

compliance_vault = ComplianceVault()
