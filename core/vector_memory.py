import os
import redis
import json

class VectorMemoryEngine:
    def __init__(self):
        redis_url = os.getenv("REDIS_URL", "redis://veritas_redis_cache:6379")
        try:
            self.client = redis.Redis.from_url(redis_url, decode_responses=True)
        except Exception:
            self.client = None

    def store_statement(self, speaker: str, statement: str, political_block: str):
        if not self.client:
            return False
        record = {
            "speaker": speaker,
            "statement": statement,
            "political_block": political_block
        }
        try:
            self.client.rpush("veritas:vector:memory", json.dumps(record))
            return True
        except Exception as e:
            print(f"Vector memory storage error: {e}")
            return False

    def query_memory(self, speaker: str) -> list:
        if not self.client:
            return []
        try:
            raw_records = self.client.lrange("veritas:vector:memory", 0, -1)
            records = [json.loads(r) for r in raw_records]
            # Filtrowanie historycznych wypowiedzi danego eksperta/polityka
            return [r for r in records if r.get("speaker") == speaker]
        except Exception as e:
            print(f"Vector memory query error: {e}")
            return []

vector_memory = VectorMemoryEngine()
