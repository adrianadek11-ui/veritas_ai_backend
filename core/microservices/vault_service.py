import logging
import time

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("VeritasVaultMicroservice")

def run_vault_service():
    log.info("[+] Mikroserwis Skarbca (Compliance & Capital Vault) gotowy i zabezpieczony.")
    while True:
        time.sleep(20)

if __name__ == "__main__":
    run_vault_service()
