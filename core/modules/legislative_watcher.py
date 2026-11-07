import asyncio
from typing import Dict, Any, List
from core.modules.pydantic_models import LegalDocumentSchema

class VeritasLegislativeWatcher:
    def __init__(self):
        # Baza monitorowania kluczowych procesów legislacyjnych i rządowych projektów
        self.legislative_db = {
            "ustawa budżetowa": {"stage": "Sejm - Trzecie czytanie", "status": "W tokach procedowania", "risk": "Wysoki spór polityczny"},
            "krajowa rada radiofonii": {"stage": "Komisja Sejmowa", "status": "Projekt w konsultacjach", "risk": "Zmiany w mediach publicznych"},
            "kodeks karny": {"stage": "Senat - Prace nad poprawkami", "status": "Oczekuje na drugie czytanie w Senacie", "risk": "Nowelizacja zaostrzająca kary"}
        }

    async def analyze_document(self, doc: LegalDocumentSchema) -> Dict[str, Any]:
        """
        Przekształcony moduł prawny: śledzi procesy legislacyjne, ustawy i rządowe projekty
        na potrzeby reżyserki Veritas Media.
        """
        await asyncio.sleep(0.01)
        findings = []
        conflicting_terms = False
        full_text = " ".join(doc.clauses).lower()

        matched_legislation = []
        for key, details in self.legislative_db.items():
            if key in full_text:
                matched_legislation.append(f"Przedmiot: {key.upper()} | Etap: {details['stage']} | Status: {details['status']} | Ryzyko: {details['risk']}")

        if not matched_legislation:
            matched_legislation.append("MONITOR SEJMOWY: Brak bezpośredniego odniesienia do kluczowych projektów rządowych w bieżącym rejestrze druków sejmowych.")

        if "uchwalona" in full_text and "podpisana" not in full_text:
            findings.append("ALARM LEGISLACYJNY: Polityk powołuje się na uchwaloną ustawę, która nie została jeszcze podpisana przez Prezydenta lub opublikowana w Dzienniku Ustaw!")
            conflicting_terms = True

        return {
            "status": "LEGISLATIVE_WATCH_SUCCESS",
            "has_contradictions": conflicting_terms,
            "audit_findings": findings if findings else ["Proces legislacyjny w normie. Brak sprzeczności w oświadczeniach."],
            "jurisprudence_grounding": matched_legislation
        }

legal_engine = VeritasLegislativeWatcher()
