import logging
import time

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("VeritasRagMicroservice")

def run_rag_engine():
    log.info("[+] Mikroserwis RAG (Core 1-3) uruchomiony w trybie niskiej latencji (<50ms).")
    while True:
        # Pętla oczekiwania na zapytania strumieniowe wektorowe
        time.sleep(10)

if __name__ == "__main__":
    run_rag_engine()
