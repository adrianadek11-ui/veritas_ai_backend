import httpx
from typing import Dict, Any, Optional

class MarketDataApi:
    """Moduł pobierający twarde dane finansowe i rynkowe z API NBP"""
    
    @staticmethod
    async def get_nbp_exchange_rate(table: str = "A", currency_code: str = "EUR") -> Optional[Dict[str, Any]]:
        url = f"https://api.nbp.pl/api/exchangerates/rates/{table}/{currency_code}/?format=json"
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    data = response.json()
                    rate = data["rates"][0]["mid"]
                    effective_date = data["rates"][0]["effectiveDate"]
                    return {
                        "status": "success",
                        "currency": data["currency"],
                        "code": data["code"],
                        "rate": rate,
                        "date": effective_date,
                        "source": f"Oficjalna tabela NBP nr {data['rates'][0]['no']} z dnia {effective_date}"
                    }
        except Exception as e:
            print(f"[MarketDataApi Error]: {e}")
        return None
