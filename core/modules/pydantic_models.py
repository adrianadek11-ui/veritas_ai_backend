from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class LegalDocumentSchema(BaseModel):
    title: str = Field(..., min_length=5)
    clauses: List[str]
    gdpr_compliant: bool = Field(default=False)
    case_signature: Optional[str] = None

class MedicalQuerySchema(BaseModel):
    prescribed_drugs: List[str]
    requested_dosage_mg: int
    patient_conditions: List[str]
