import asyncio
import time
from core.radio_stream import radio_stream
from core.darknet_sentinel import darknet_sentinel
from core.dynamic_growth_matrix import dynamic_growth
from core.api_bridge import api_bridge

async def autonomous_background_loop():
    print("🤖 [DEMON TŁA VERITAS] Uruchomiono autonomiczny cykl nasłuchu i propagacji...")
    while True:
        try:
            # 1. Nasłuch strumieni w tle
            radio_data = radio_stream.process_radio_feed()
            darknet_data = darknet_sentinel.scan_passive_feeds()
            
            # 2. Jeśli wykryto wysoki priorytet, automatyczny spawn
            dynamic_growth.spawn_viral_satellite_network("Autonomous Background Sentinel Sweep", 91.5)
            
            # 3. Krótki sleep przed kolejnym cyklem
            await asyncio.sleep(30)
        except Exception as e:
            print(f"⚠️ [DEMON BŁĄD]: {e}")
            await asyncio.sleep(10)
