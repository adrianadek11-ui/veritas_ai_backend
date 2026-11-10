import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("SelfSustainingOPEX")

class OPEXAutoFund:
    def __init__(self, reinvestment_rate: float = 0.05):
        self.reinvestment_rate = reinvestment_rate  # 5% zysków na infrastrukturę
        log.info(f"[*] Self-Sustaining OPEX aktywny. Automatyczne dożywianie proxy: {self.reinvestment_rate * 100}%.")

    def process_incoming_revenue(self, revenue_usd: float):
        allocated_for_proxy = revenue_usd * self.reinvestment_rate
        log.info(f"[OPEX] Przychód: ${revenue_usd:.2f} | Automatycznie zasilono fundusz proxy: ${allocated_for_proxy:.2f}")
        return allocated_for_proxy

if __name__ == "__main__":
    fund = OPEXAutoFund()
    fund.process_incoming_revenue(2500.0)
