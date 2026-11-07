#!/bin/bash
echo "=== [VERITAS MEDIA] Czyszczenie portu 8000... ==="
sudo fuser -k 8000/tcp 2>/dev/null
kill -9 $(lsof -t -i:8000) 2>/dev/null
sleep 1

echo "=== [VERITAS MEDIA] Uruchamianie serwera FastAPI w tle (Nano-Core)... ==="
nohup uvicorn main:app --reload --port 8000 > server.log 2>&1 &

echo "=== [VERITAS MEDIA] Serwer wystartował pomyślnie na http://127.0.0.1:8000 ==="
echo "Możesz podejrzeć logi poleceniem: tail -f server.log"
