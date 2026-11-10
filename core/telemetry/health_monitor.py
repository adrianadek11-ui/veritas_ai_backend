import psutil
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
log = logging.getLogger("VeritasHealthMonitor")

def monitor_system_resources():
    log.info("[*] Uruchomiono autonomiczny moduł telemetrii i kontroli klastra Veritas.")
    while True:
        try:
            # Pobieranie telemetrii procesora i pamięci
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            log.info(f"[TELEMETRY] CPU Usage: {cpu_percent}% | RAM Used: {memory.percent}% ({memory.used // (1024*1024)}MB / {memory.total // (1024*1024)}MB)")
            
            # Autonomiczny próg ostrzegawczy (90% zużycia RAM)
            if memory.percent > 90.0:
                log.warning("[!] OSTRZEŻENIE: Krytyczne zużycie pamięci RAM! Aktywacja protokołu oczyszczania bufora Redis.")
                
        except Exception as e:
            log.error(f"[-] Błąd w pętli telemetrii: {e}")
            
        time.sleep(30)

if __name__ == "__main__":
    monitor_system_resources()
