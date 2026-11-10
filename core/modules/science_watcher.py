import asyncio
from typing import Dict, Any, List
from core.modules.pydantic_models import MedicalQuerySchema

class VeritasFactAndScienceCheckEngine:
    def __init__(self):
        # Baza faktów naukowych, biologicznych, przyrodniczych i statystycznych
        self.science_database = {
            "żubr": {
                "fact": "Żubry to duże ssaki lądowe, które poruszają się po ziemi. Nie wchodzą na drzewa i nie łamią nóg na gałęziach.",
                "category": "Biologia / Zoologia",
                "severity": "Absurd przyrodniczy"
            },
            "szczepienia": {
                "fact": "Szczepienia są powszechnie przebadanymi procedurami medycznymi opartymi na rygorystycznych badaniach klinicznych (EBM).",
                "category": "Medycyna / Zdrowie Publiczne",
                "severity": "Weryfikacja kliniczna"
            },
            "klimat": {
                "fact": "Zmiany klimatyczne są udokumentowane empirycznie przez niezależne ośrodki naukowe na całym świecie.",
                "category": "Nauki o Ziemi / Ekologia",
                "severity": "Fakt naukowy"
            }
        }

    async def verify_clinical_safety(self, medical_req: MedicalQuerySchema) -> Dict[str, Any]:
        """
        Przekształcony moduł naukowo-faktyczny: weryfikuje tezy biologiczne, 
        przyrodnicze i medyczne na potrzeby reżyserki Veritas Media.
        """
        await asyncio.sleep(0.01)
        warnings = []
        patient_conditions = [c.lower() for c in medical_req.patient_conditions]
        
        # Analiza przepisanych substancji/zagadnień pod kątem absurdów naukowych
        combined_text = " ".join(patient_conditions + medical_req.prescribed_drugs).lower()

        matched_facts = []
        for keyword, data in self.science_database.items():
            if keyword in combined_text:
                matched_facts.append(f"Kategoria: {data['category']} | Fakt: {data['fact']} | Ocena: {data['severity']}")
                if data['severity'] == "Absurd przyrodniczy":
                    warnings.append(f"🚨 ALARM NAUKOWY: Wykryto wypowiedź naruszającą podstawowe prawa biologii/przyrody w zakresie hasła '{keyword}'!")

        if not matched_facts:
            matched_facts.append("FAKTOGRAFIA NAUKOWA: Brak bezpośrednich zastrzeżeń w lokalnym rejestrze tez naukowych. Wymaga standardowej weryfikacji RAG.")

        return {
            "status": "SCIENCE_VERIFICATION_COMPLETE",
            "clinical_alerts": warnings if warnings else ["Brak wykrytych absurdów naukowych w bieżącej wypowiedzi."],
            "differential_diagnosis_assistance": matched_facts,
            "compliance_standard": "Standard Naukowy / Oparte na Dowodach (EBM)"
        }

medical_engine = VeritasFactAndScienceCheckEngine()
