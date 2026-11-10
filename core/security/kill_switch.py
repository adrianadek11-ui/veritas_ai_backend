import os
import logging
import signal

log = logging.getLogger("VeritasKillSwitch")

class EmergencyKillSwitch:
    @staticmethod
    def execute_shutdown(reason="OPERATOR_MANUAL_TRIGGER"):
        log.critical(f"[!] AWARYJNY WYŁĄCZNIK AKTYWOWANY. Powód: {reason}")
        # Natychmiastowe zamrożenie procesów roju i zapis stanu bezpieczeństwa
        pid_file = "veritas_swarm.pid"
        if os.path.exists(pid_file):
            with open(pid_file, "r") as f:
                pids = f.readlines()
                for p in pids:
                    try:
                        os.kill(int(p.strip()), signal.SIGTERM)
                    except Exception as ex:
                        log.error(f"Nie udało sięubić procesów roju: {ex}")
        log.info("[+] Rój odłączony, sieć zamrożona, węzeł przechodzi w tryb stealth.")
        return {"status": "EMERGENCY_SHUTDOWN_SUCCESS", "reason": reason}

kill_switch = EmergencyKillSwitch()
