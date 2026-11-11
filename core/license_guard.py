import os
import sys
import logging
import platform
import subprocess
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [LICENSE_GUARD] - %(message)s')

LICENSE_FILE = "core/security_vault/license.key"
HWID_FILE = "core/security_vault/machine.hwid"
TRIAL_DAYS = 7

def get_hardware_fingerprint():
    """Generuje unikalny odcisk palca maszyny na podstawie parametrów systemowych."""
    try:
        # Próbujemy pobrać unikalny identyfikator maszyny z systemu
        if os.path.exists("/etc/machine-id"):
            with open("/etc/machine-id", "r") as f:
                return f.read().strip()
        # Alternatywnie bazujemy na nazwie hosta i architekturze procesora
        hw_info = platform.node() + platform.processor() + platform.machine()
        return str(abs(hash(hw_info)))
    except Exception:
        return "VERITAS-FALLBACK-HWID"

def verify_operational_license():
    logging.info("Weryfikacja uprawnień i statusu licencji Veritas...")
    
    current_hwid = get_hardware_fingerprint()
    
    # 1. Sprawdzenie, czy istnieje pełna, stała licencja
    if os.path.exists(LICENSE_FILE):
        try:
            with open(LICENSE_FILE, "r") as f:
                lines = f.readlines()
            
            expiry_date_str = lines[0].strip().split("=")[1]
            expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d")
            
            if datetime.now() > expiry_date:
                logging.critical("BLOKADA BEZPIECZEŃSTWA: Stała licencja operacyjna wygasła. Wymagane odnowienie u Architekta.")
                sys.exit(1)
                
            logging.info("Stała licencja operacyjna ważna. System działa w autoryzowanym reżimie.")
            return
        except Exception as e:
            logging.error(f"Błąd walidacji pliku stałej licencji: {e}. System zablokowany.")
            sys.exit(1)

    # 2. Jeśli brak stałej licencji -> Obsługa 7-dniowego Trybu Próbnego (Trial) powiązanego ze sprzętem
    os.makedirs("core/security_vault", exist_ok=True)
    
    if not os.path.exists(HWID_FILE):
        # Pierwsze uruchomienie na tej maszynie! Zapisujemy HWID i datę startu trialu
        trial_end_date = datetime.now() + timedelta(days=TRIAL_DAYS)
        try:
            with open(HWID_FILE, "w") as f:
                f.write(f"HWID={current_hwid}\n")
                f.write(f"TRIAL_END={trial_end_date.strftime('%Y-%m-%d')}\n")
            os.chmod(HWID_FILE, 0o600)
            logging.info(f"Inicjalizacja 7-dniowego okresu próbnego (Trial). Wygasa: {trial_end_date.strftime('%Y-%m-%d')}")
        except Exception as e:
            logging.critical(f"Nie udało się zapisać danych trialu: {e}")
            sys.exit(1)
    else:
        # Odczytujemy zapisany trial i weryfikujemy HWID
        try:
            with open(HWID_FILE, "r") as f:
                hwid_lines = f.readlines()
            
            saved_hwid = hwid_lines[0].strip().split("=")[1]
            trial_end_str = hwid_lines[1].strip().split("=")[1]
            trial_end_date = datetime.strptime(trial_end_str, "%Y-%m-%d")
            
            # Twarde sprawdzenie czy ktoś nie przełożył dysku / pendrive'a na inny komputer
            if saved_hwid != current_hwid:
                logging.critical("KRYTYCZNY BŁĄD BEZPIECZEŃSTWA: Wykryto próbę uruchomienia na nieautoryzowanym sprzęcie (Machine Hopping Zablokowany).")
                sys.exit(1)
                
            # Sprawdzenie czy minęło 7 dni
            if datetime.now() > trial_end_date:
                logging.critical("BLOKADA BEZPIECZEŃSTWA: 7-dniowy okres próbny wygasł. Wymagany kontakt z Architektem i aktywacja licencji.")
                sys.exit(1)
                
            remaining_days = (trial_end_date - datetime.now()).days
            logging.info(f"System działa w trybie próbnym (Trial). Pozostało dni: {max(0, remaining_days + 1)}")
            
        except Exception as e:
            logging.error(f"Błąd weryfikacji pliku trialu: {e}. System zablokowany.")
            sys.exit(1)

if __name__ == "__main__":
    verify_operational_license()
