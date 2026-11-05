from typing import Dict, Any, List

class FlipFlopDetector:
    """Moduł wykrywający zmianę stanowisk polityków (retoryczne wolty) w czasie"""
    
    @staticmethod
    def analyze_statement(current_statement: str, historical_records: List[str]) -> Dict[str, Any]:
        """Porównuje bieżącą wypowiedź z historycznymi wpisami / wypowiedziami"""
        conflicts = []
        for record in historical_records:
            # Uproszczona analiza semantyczna / symulacja wykrycia sprzeczności
            if len(current_statement) > 5 and any(word in record.lower() for word in ["zawsze", "nigdy", "popieram", "odrzucam"]):
                conflicts.append({
                    "past_statement": record,
                    "discrepancy_level": "Wysoka",
                    "summary": "Wykryto potencjalną woltę retoryczną względem wcześniejszego stanowiska."
                })
                
        return {
            "has_flipped": len(conflicts) > 0,
            "conflicts": conflicts
        }
