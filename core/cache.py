import time
from collections import OrderedDict
from typing import Any, Optional

class SmartCache:
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        self.cache: OrderedDict[str, tuple[Any, float]] = OrderedDict()
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds

    def get(self, key: str) -> Optional[Any]:
        if key not in self.cache:
            return None
        
        value, timestamp = self.cache[key]
        
        # Sprawdzenie czy wpis wygasł (TTL)
        if time.time() - timestamp > self.ttl_seconds:
            del self.cache[key]
            return None
            
        # Przeniesienie na koniec (LRU - najnowsze użycie)
        self.cache.move_to_end(key)
        return value

    def set(self, key: str, value: Any) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.max_size:
            # Usuwamy najstarszy element (FIFO/LRU eviction)
            self.cache.popitem(last=False)
            
        self.cache[key] = (value, time.time())

    def clear(self) -> None:
        self.cache.clear()
