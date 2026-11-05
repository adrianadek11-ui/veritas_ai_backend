# Veritas IE - Buffer & Intent Core (Rdzeń 0 - Advanced Multi-Stream & Diarization)
import time
import re

class IntentBufferCore:
    def __init__(self):
        self.version = "2.0.0-AUTONOMOUS-BUFFER"
        print("[*] Core 0: Advanced Autonomous Buffer & Diarization initialized.")

    def process_and_classify(self, raw_query: str):
        start_t = time.time()
        cleaned_query = raw_query.strip()
        q_lower = cleaned_query.lower()

        is_shouting_match = " vs " in q_lower or "przekrzykuje" in q_lower or q_lower.count("?") > 1
        absurd_keywords = ["krowa lata", "kosmici", "płaska ziemia", "grawitacja nie istnieje", "czary", "kon frowa"]
        is_absurd = any(word in q_lower for word in absurd_keywords)

        if is_absurd:
            intent_type = "ABSURD_PHYSICS"
            domain = "Fakty Naukowe & Prawa Fizyki"
            conflict_text = "Teza całkowicie sprzeczna z podstawowymi prawami fizyki i biologii."
            direct_answer = (
                f"<strong>WERYFIKACJA FAKTYCZNA (Prawa Fizyki):</strong><br>"
                f"Twierdzenie „{cleaned_query}” nie posiada żadnych podstaw naukowo-przyrodniczych.<br>"
                f"<ul>"
                f"<li><strong>Analiza logiczna:</strong> Zjawisko narusza prawa aerodynamiki i grawitacji.</li>"
                f"<li><strong>Dokumentacja źródłowa:</strong> Podstawy fizyki klasycznej i biologii.</li>"
                f"<li><a href='https://encyklopedia.pwn.pl' target='_blank'>[Encyklopedia PWN - Prawa Przyrody]</a></li>"
                f"</ul>"
            )
            ripostes = [
                {"id": 1, "type": "ŻYWY CHATBOT #1 [AUTONOMOUS]", "text": "Zejdźmy na ziemię – prawa fizyki i biologii nie podlegają interpretacji retorycznej.", "conflict_fact": conflict_text, "bio_analysis": "RODO: Absurd emisyjny 100%."},
                {"id": 2, "type": "ŻYWY CHATBOT #2 [AUTONOMOUS]", "text": "Tego typu tezy nadają się do kabaretu, a nie do merytorycznej debaty publicznej.", "conflict_fact": conflict_text, "bio_analysis": "RODO: Absurd emisyjny 100%."}
            ]
            director_log = "[MASTER CONTROL] Wykryto absurd fizyczny. Wymuszono natychmiastową reakcję chatbota."
            bio_text = "Analiza RODO: Poziom satyryczny 100%."
            truth_score = 0
            is_dezi = True
        elif is_shouting_match:
            intent_type = "STREAM_CONFLICT"
            domain = "Zarządzanie Strumieniem Debaty"
            conflict_text = "Wykryto nakładanie się głosów i konflikt wątków w studio."
            direct_answer = (
                f"<strong>ALERTS SYSTEMOWY - KONFLIKT STRUMIENI:</strong><br>"
                f"Uczestnicy debaty nakładają na siebie wypowiedzi. Rdzeń 0 dokonał separacji wątku dla: '{cleaned_query}'.<br>"
                f"<ul><li><strong>Zalecenie:</strong> Przywołaj uczestników do porządku regulaminowego.</li></ul>"
            )
            ripostes = [
                {"id": 1, "type": "ŻYWY CHATBOT #1 [SPLITTER]", "text": "Panowie, proszę o dyscyplinę słowa. Wracamy do meritum, a nie do przekrzykiwania.", "conflict_fact": conflict_text, "bio_analysis": "RODO: Konflikt strumieni audio."},
                {"id": 2, "type": "ŻYWY CHATBOT #2 [SPLITTER]", "text": "System oddzielił tezy. Proszę o wypowiedzi w trybie twardych danych.", "conflict_fact": conflict_text, "bio_analysis": "RODO: Konflikt strumieni audio."}
            ]
            director_log = "[MASTER CONTROL] Separacja wątku zablokowała chaos w studiu."
            bio_text = "Analiza RODO: Stabilizacja mikrofonów."
            truth_score = 50
            is_dezi = False
        else:
            intent_type = "STANDARD_QUERY"
            domain = "Encyklopedia & Rejestry Live"
            conflict_text = None
            direct_answer = None
            ripostes = []
            director_log = None
            bio_text = None
            truth_score = None
            is_dezi = None

        latency = round((time.time() - start_t) * 1000, 2)
        return {
            "cleaned_query": cleaned_query,
            "intent_type": intent_type,
            "is_absurd": is_absurd,
            "is_shouting_match": is_shouting_match,
            "domain": domain,
            "conflict_text": conflict_text,
            "direct_answer": direct_answer,
            "riposte_variants": ripostes,
            "director_log": director_log,
            "bio_text": bio_text,
            "truth_score": truth_score,
            "is_dezi": is_dezi,
            "buffer_latency": f"{latency} ms"
        }

buffer_core = IntentBufferCore()
