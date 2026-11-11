import os
import shutil
import sys
import time

def execute_atomic_destructor(confirmation_code):
    # Wymagany unikalny klucz awaryjny znany tylko Architektowi
    if confirmation_code != "VERITAS-OMEGA-KILL-99":
        print("BŁĘDNY KOD AUTORYZACJI. Destrukcja odrzucona.")
        return

    print(">>> OSTRZEŻENIE: INICJALIZACJA PROTOKOŁU ATOMOWEGO VERITAS <<<")
    time.sleep(1)
    
    targets = [
        "core/security_vault/",
        "core/ally_network/",
        "core/sentinel_logs/",
        "core/.env",
        "core/state_cache/"
    ]

    for target in targets:
        if os.path.exists(target):
            if os.path.isdir(target):
                shutil.rmtree(target, ignore_errors=True)
            else:
                os.remove(target)
            print(f"Zneutralizowano zasób: {target}")

    # Nadpisanie losowymi bajtami pliku głównego
    core_files = [f for f in os.listdir("core") if f.endswith(".py")]
    for file in core_files:
        filepath = os.path.join("core", file)
        try:
            with open(filepath, "wb") as f:
                f.write(os.urandom(4096))
            print(f"Nadpisano kryptograficznym szumem: {filepath}")
        except Exception:
            pass

    print(">>> SYSTEM ZDESTRUKTOWANY. BRAK ŚLADÓW. ZEGARY WYZEROWANE. <<<")
    sys.exit(0)

if __name__ == "__main__":
    code = input("Podaj kod autoryzacji ostatecznej destrukcji: ")
    execute_atomic_destructor(code)
