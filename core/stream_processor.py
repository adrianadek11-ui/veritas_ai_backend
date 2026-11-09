import os
import redis
import json

class StreamProcessor:
    def __init__(self):
        redis_url = os.getenv("REDIS_URL", "redis://veritas_redis_cache:6379")
        try:
            self.client = redis.Redis.from_url(redis_url, decode_responses=True)
            self.stream_name = "veritas:stream:events"
        except Exception:
            self.client = None

    def push_event(self, event_type: str, payload: dict) -> str:
        if not self.client:
            return "NO_REDIS"
        data = {
            "event_type": event_type,
            "payload": json.dumps(payload)
        }
        try:
            msg_id = self.client.xadd(self.stream_name, data)
            return msg_id
        except Exception as e:
            print(f"Stream push error: {e}")
            return "ERROR"

stream_processor = StreamProcessor()
