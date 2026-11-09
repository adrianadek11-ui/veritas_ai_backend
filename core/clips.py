import json

class AutoClipsGenerator:
    def generate_viral_clip_package(self, query: str, brain_result: dict) -> dict:
        answer = brain_result.get("direct_answer", "")
        signature = brain_result.get("nda_governance", {}).get("signature", "VERIFIED")
        
        # Formatowanie pod krótkie formy / social media (Viral Loop)
        clip_package = {
            "format": "VERTICAL_SHORT_9_16",
            "headline": f"🚨 VERITAS ALERT: {query}",
            "key_takeaway": answer.split("\n")[0] if answer else query,
            "anchor_quotes": brain_result.get("anchor_munition", []),
            "trust_badge": "VERIFIED BY COMPLIANCE VAULT",
            "cryptographic_proof": signature,
            "distribution_channels": ["TikTok", "Instagram Reels", "YouTube Shorts", "X (Twitter) Feed"]
        }
        return clip_package

clips_generator = AutoClipsGenerator()
