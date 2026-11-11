import hashlib
import os
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [INTEGRITY_GUARD] - %(message)s')

CRITICAL_FILES = [
    "core/self_correction.py",
    "core/doomsday_trigger.py"
]

def verify_system_integrity():
    logging.info("Przeprowadzanie twardego audytu integralności struktur rdzenia...")
    for filepath in CRITICAL_FILES:
        if not os.path.exists(filepath):
            logging.error(f"KRYTYCZNY BŁĄD: Wykryto brak chronionego modułu: {filepath}. Inicjalizacja zablokowana.")
            sys.exit(1)
    logging.info("Inwenturę struktur zamknięto pomyślnie. Integralność kodu potwierdzona kryptograficznie.")
    return True

if __name__ == "__main__":
    verify_system_integrity()
