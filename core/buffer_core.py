import logging

logger = logging.getLogger("DebateBuffer")

class DebateBuffer:
    def __init__(self):
        self.history = []
        logger.info("[*] Core 0: Advanced Autonomous Buffer & Diarization initialized.")

    def add_entry(self, speaker: str, text: str):
        self.entry = {"speaker": speaker, "text": text}
        self.history.append(self.entry)
        return self.entry

debate_buffer = DebateBuffer()
