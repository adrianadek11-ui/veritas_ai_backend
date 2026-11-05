import asyncio
import json
from typing import AsyncGenerator

class ResultStreamer:
    @staticmethod
    async def event_generator(data_stream: list[str]) -> AsyncGenerator[str, None]:
        """Generator strumieniowy SSE wysyłający fragmenty danych słowo po słowie / chunk po chunku."""
        for chunk in data_stream:
            # Symulacja strumieniowania na żywo dla frontendu
            yield f"data: {json.dumps({'status': 'streaming', 'content': chunk})}\n\n"
            await asyncio.sleep(0.05)  # płynna mikro-pauza dla efektu live
        
        yield f"data: {json.dumps({'status': 'completed'})}\n\n"
