import logging
from typing import Dict, Any, List
from datetime import datetime

log = logging.getLogger("VeritasCommandEngine")

class CommandEngine:
    def __init__(self):
        self.custom_commands: Dict[str, str] = {
            "STOP_ALL": "Natychmiastowe zamrożenie wszystkich rojów tła i krypto.",
            "BOOST_CRYPTO": "Zwiększenie alokacji kapitałowej dla bezpiecznych okazji z Confidence > 80%.",
            "AUDIT_SYSTEM": "Pełny zrzut certyfikatów SHA-256 z Compliance Vault."
        }
        log.info("Veritas Command Engine (Rejestr Komend i Głosowy Asystent) aktywny.")

    def register_command(self, cmd_name: str, action_desc: str) -> Dict[str, Any]:
        """Pozwala operatorowi dodać nową komendę w locie."""
        self.custom_commands[cmd_name] = action_desc
        log.info(f"[CommandEngine] Zarejestrowano nową komendę operatora: {cmd_name} -> {action_desc}")
        return {"status": "COMMAND_REGISTERED", "command": cmd_name, "total_commands": len(self.custom_commands)}

    def execute_command(self, cmd_name: str) -> Dict[str, Any]:
        """Wykonuje zarejestrowaną komendę lub zgłasza błąd nieznanej intencji."""
        if cmd_name in self.custom_commands:
            log.info(f"[CommandEngine] Wykonywanie komendy operatora: {cmd_name}")
            return {
                "status": "EXECUTED",
                "command": cmd_name,
                "description": self.custom_commands[cmd_name],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        else:
            log.warning(f"[CommandEngine] Próba wykonania nieznanej komendy: {cmd_name}")
            return {"status": "UNKNOWN_COMMAND", "command": cmd_name}

command_engine = CommandEngine()
