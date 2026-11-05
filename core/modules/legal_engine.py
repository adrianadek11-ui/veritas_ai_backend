import asyncio
from typing import Dict, Any, List
from core.modules.pydantic_models import LegalDocumentSchema

class VeritasLegalEngine:
    def __init__(self):
        self.jurisprudence_db = {
            "sn_ii_csk": "Orzecznictwo Sądu Najwyższego (Izba Cywilna): Zapisy abuzywne są nieważne ab initio.",
            "nsa_i_fsk": "Naczelny Sąd Administracyjny: Obowiązek należytej staranności w transakcjach VAT.",
            "ksh_art_201": "Kodeks Spółek Handlowych: Odpowiedzialność członków zarządu za zobowiązania spółki."
        }

    async def analyze_document(self, doc: LegalDocumentSchema) -> Dict[str, Any]:
        await asyncio.sleep(0.01)
        findings, conflicting_terms = [], False
        full_text = " ".join(doc.clauses).lower()
        if "wyłączna odpowiedzialność" in full_text and "brak odpowiedzialności" in full_text:
            findings.append("WYKRYTO SPRZECZNOŚĆ LOGICZNĄ: Wykluczające się zapisy o odpowiedzialności.")
            conflicting_terms = True
        if not doc.gdpr_compliant:
            findings.append("ALARM ZGODNOŚCI: Brak klauzuli RODO/GDPR.")
        matched_jurisprudence = []
        if doc.case_signature:
            sig_clean = doc.case_signature.lower().replace(" ", "_")
            for key, reference in self.jurisprudence_db.items():
                if key in sig_clean: matched_jurisprudence.append(reference)
        if not matched_jurisprudence: matched_jurisprudence.append("Zastosowano wykładnię ogólną prawa handlowego.")
        return {"status": "LEGAL_ANALYSIS_SUCCESS", "has_contradictions": conflicting_terms, "audit_findings": findings if findings else ["Dokument formalnie spójny."], "jurisprudence_grounding": matched_jurisprudence}

legal_engine = VeritasLegalEngine()
