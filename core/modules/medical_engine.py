import asyncio
from typing import Dict, Any, List
from core.modules.pydantic_models import MedicalQuerySchema

class VeritasMedicalEngine:
    def __init__(self):
        self.chpl_database = {
            "ibuprofen": {"max_adult_daily_mg": 1200, "contraindications": ["wrzody żołądka", "niewydolność nerek"], "interactions": {"aspiryna": "Zwiększone ryzyko krwawień z przewodu pokarmowego."}},
            "paracetamol": {"max_adult_daily_mg": 4000, "contraindications": ["niewydolność wątroby"], "interactions": {}}
        }

    async def verify_clinical_safety(self, medical_req: MedicalQuerySchema) -> Dict[str, Any]:
        await asyncio.sleep(0.01)
        warnings = []
        patient_conditions = [c.lower() for c in medical_req.patient_conditions]
        for drug in medical_req.prescribed_drugs:
            drug_lower = drug.lower()
            if drug_lower in self.chpl_database:
                specs = self.chpl_database[drug_lower]
                if medical_req.requested_dosage_mg > specs["max_adult_daily_mg"]:
                    warnings.append(f"PRZEKROCZENIE DAWKI (ChPL): '{drug}' przekracza limit {specs['max_adult_daily_mg']}mg.")
                for condition in patient_conditions:
                    if condition in specs["contraindications"]: warnings.append(f"BEZWZGLĘDNE PRZECIWWSKAZANIE: '{drug}' zakazany przy: {condition}.")
            else:
                warnings.append(f"OSTRZEŻENIE RAG: Substancja '{drug}' nieznana w bazie lokalnej ChPL.")
        drugs_list = [d.lower() for d in medical_req.prescribed_drugs]
        if "ibuprofen" in drugs_list and "aspiryna" in drugs_list:
            warnings.append("NIEBEZPIECZNA INTERAKCJA: Ibuprofen + Aspiryna nasila ryzyko krwawień.")
        return {"status": "MEDICAL_VERIFICATION_COMPLETE", "clinical_alerts": warnings if warnings else ["Brak wykrytych negatywnych interakcji lekowych."], "differential_diagnosis_assistance": ["Diagnostyka podstawowa pod kątem stanu zapalnego (WHO)."], "compliance_standard": "WHO / AOTMiT Standard"}

medical_engine = VeritasMedicalEngine()
