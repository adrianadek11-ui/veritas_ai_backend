from typing import Dict, Any

class VoiceEmotionAnalyzer:
    """Moduł analizy paralingwistycznej i języka ciała (audio/video feed)"""
    
    @staticmethod
    def analyze_audio_stream(pitch_variance: float, speech_tempo: float) -> Dict[str, Any]:
        """Ocenia poziom stresu i napięcia na podstawie głosu w studiu"""
        stress_level = "Niski"
        if pitch_variance > 0.7 or speech_tempo > 140:
            stress_level = "Wysoki"
        elif pitch_variance > 0.4:
            stress_level = "Umiarkowany"
            
        return {
            "stress_level": stress_level,
            "pitch_variance": pitch_variance,
            "speech_tempo": speech_tempo,
            "evasion_detected": stress_level == "Wysoki"
        }
