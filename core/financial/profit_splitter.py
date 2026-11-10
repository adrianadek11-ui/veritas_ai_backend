import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("ProfitSplitterEngine")

class ProfitSplitter:
    def __init__(self, operational_share: float = 0.30, vault_share: float = 0.70):
        self.operational_share = operational_share  # np. 30% na bieżące proxy i serwery
        self.vault_share = vault_share              # 70% do bezpiecznego skarbca / rezerwy
        log.info("[*] Profit Splitter Engine zainicjalizowany. Tryb alokacji: 30% Op / 70% Vault.")

    def distribute_revenue(self, total_revenue_usd: float):
        op_funds = total_revenue_usd * self.operational_share
        vault_funds = total_revenue_usd * self.vault_share
        
        log.info(f"[FINANCE] Przychód całkowity: ${total_revenue_usd:.2f}")
        log.info(f" -> Alokacja na koszty operacyjne (proxy/infrastruktura): ${op_funds:.2f}")
        log.info(f" -> Alokacja do skarbca (Vault / BTC Reserve): ${vault_funds:.2f}")
        
        return {"operational": op_funds, "vault": vault_funds}

if __name__ == "__main__":
    splitter = ProfitSplitter()
    splitter.distribute_revenue(1000.0)
