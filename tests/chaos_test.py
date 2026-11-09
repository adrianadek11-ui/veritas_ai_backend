import asyncio
import aiohttp
import time

async def send_request(session, query_text):
    url = "http://localhost:8000/query"
    headers = {
        "Authorization": "Bearer veritas-secret-secure-token-f1",
        "Content-Type": "application/json"
    }
    payload = {"query": query_text}
    async with session.post(url, json=payload, headers=headers) as response:
        return response.status

async def run_chaos_simulation():
    print("🚀 [CHAOS ENGINE] Start symulacji obciążeniowej: 50 równoległych strumieni studio...")
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, f"Test obciążeniowy strumienia #{i}") for i in range(50)]
        results = await asyncio.gather(*tasks)
    duration = time.time() - start_time
    print(f"✅ [CHAOS ENGINE] Zakończono! Przetworzono {len(results)} zapytań w czasie {duration:.2f} sekund.")

if __name__ == "__main__":
    asyncio.run(run_chaos_simulation())
