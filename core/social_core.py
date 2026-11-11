import asyncio
from typing import List, Dict, Any

class SocialWatcherCore:
    """Rdzeń odpowiedzialny za monitorowanie wskazanych kont w social mediach w czasie rzeczywistym"""
    
    def __init__(self, target_accounts: List[str] = None):
        # Domyślna lista monitorowanych kont (whitelist)
        self.target_accounts = target_accounts or ["@SejmRP", "@KPRM_PB", "@PremierRP"]
        self.cached_posts: List[Dict[str, Any]] = []

    async def fetch_latest_posts(self, keyword: str = "") -> List[Dict[str, Any]]:
        """Symulacja nasłuchu i filtrowania najnowszych wpisów pod kątem słowa kluczowego z debaty"""
        # W produkcyjnym środowisku miejsce na zapytanie do API X/Twitter / RSS / Webhooka
        matched_alerts = []
        
        # Przykładowy format wpisu trafiający na żywo do reżyserki
        if keyword:
            matched_alerts.append({
                "account": "@PrzykładowyPolitik",
                "platform": "X/Twitter",
                "timestamp": "przed chwilą",
                "content": f"Oficjalne oświadczenie w sprawie: {keyword}. Twierdzimy zupełnie co innego niż w studiu!",
                "relevance_score": 0.95,
                "suggested_action": f"Daj prowadzącemu: Spytaj o ten wpis w kontekście {keyword}"
            })
            
        return matched_alerts
