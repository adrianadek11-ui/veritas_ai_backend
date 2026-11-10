import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("ConsoleDevKitSpoofer")

class ConsoleTrafficSpoofer:
    def __init__(self, console_type: str = "PS5-Streaming-SDK"):
        self.console_type = console_type
        log.info(f"[*] PlayStation / Xbox DevKit Spoofer aktywny. Profil emulacji: {self.console_type}")

    def inject_headers(self, request_headers: dict) -> dict:
        spoofed_headers = request_headers.copy()
        spoofed_headers["User-Agent"] = "Mozilla/5.0 (PlayStation 5/2.26) AppleWebKit/605.1.15 (KHTML, like Gecko)"
        spoofed_headers["X-DevKit-Platform"] = "Sony-Interactive-Entertainment/PS5"
        spoofed_headers["X-Connection-Type"] = "Ethernet-Gigabit"
        
        log.info("[SPOOF] Pomyślnie podmieniono nagłówki sieciowe na sygnaturę konsoli do gier.")
        return spoofed_headers

if __name__ == "__main__":
    spoofer = ConsoleTrafficSpoofer()
    dummy_headers = {"User-Agent": "python-requests/2.28"}
    spoofer.inject_headers(dummy_headers)
