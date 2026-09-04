#!/bin/bash
echo "===== TESTY LUNA v5.1 ====="
echo ""

echo "[1/5] TEST SPEED - hej (ma byc <10s i Cześć)"
time curl -s -X POST http://127.0.0.1:8082/api/chat -H "Content-Type: application/json" -d '{"message":"hej"}'
echo -e "\n"

echo "[2/5] TEST ANTI-HALUCYNACJA - folder (ma byc 0.02s i prawdziwe pliki, bez plik1.txt)"
time curl -s -X POST http://127.0.0.1:8082/api/chat -H "Content-Type: application/json" -d '{"message":"co masz w folderze?"}' | head -c 500
echo -e "\n"

echo "[3/5] TEST PAMIEC - imie"
curl -s -X POST http://127.0.0.1:8082/api/chat -H "Content-Type: application/json" -d '{"message":"jestem Krzysztof i lubie testy"}' | jq -r .reply
sleep 1
curl -s -X POST http://127.0.0.1:8082/api/chat -H "Content-Type: application/json" -d '{"message":"jak mam na imie?"}' | jq -r .reply
echo ""

echo "[4/5] TEST LOGIKA - 2+2"
curl -s -X POST http://127.0.0.1:8082/api/chat -H "Content-Type: application/json" -d '{"message":"ile to 2+2? odpowiedz krotko"}' | jq -r .reply
echo ""

echo "[5/5] TEST STATUS"
curl -s http://127.0.0.1:8082/api/status | jq
echo ""
echo "===== KONIEC TESTOW ====="
echo "Sprawdz tez w przegladarce: http://127.0.0.1:8082"
echo "CTRL+F5 zeby odswiezyc cache po fixie"
