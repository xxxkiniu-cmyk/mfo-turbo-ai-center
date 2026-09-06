#!/usr/bin/env bash
set -u

PROJECT="$HOME/mfo/mfo-turbo-ai-center"
MODEL="$HOME/mfo-models/Qwen2.5-Coder-3B-Instruct-Q4_K_M.gguf"
LLAMA="http://127.0.0.1:1234"
WEB="http://127.0.0.1:8082"

PASS=0
FAIL=0

ok() {
    echo "✅ PASS: $1"
    PASS=$((PASS+1))
}

bad() {
    echo "❌ FAIL: $1"
    FAIL=$((FAIL+1))
}

echo
echo "===================================="
echo " MFO TURBO AI CENTER — TEST v6.0"
echo "===================================="
echo

echo "[1/6] llama-server..."
if curl -fsS "$LLAMA/health" 2>/dev/null | grep -q '"ok"'; then
    ok "llama-server /health"
else
    bad "llama-server /health"
fi

echo
echo "[2/6] Model GGUF..."
MODELS="$(curl -fsS "$LLAMA/v1/models" 2>/dev/null || true)"
if printf '%s' "$MODELS" | grep -q 'Qwen2.5-Coder-3B-Instruct-Q4_K_M.gguf'; then
    ok "Qwen2.5-Coder-3B widoczny"
else
    bad "Qwen2.5-Coder-3B niewidoczny"
fi

echo
echo "[3/6] Bezpośredni chat llama-server..."
DIRECT="$(curl -fsS "$LLAMA/v1/chat/completions" \
  -H 'Content-Type: application/json' \
  -d "{
    \"model\":\"$MODEL\",
    \"messages\":[{\"role\":\"user\",\"content\":\"Reply exactly MFO_DIRECT_OK\"}],
    \"temperature\":0,
    \"max_tokens\":32,
    \"stream\":false
  }" 2>/dev/null || true)"

if printf '%s' "$DIRECT" | grep -q 'MFO_DIRECT_OK'; then
    ok "bezpośrednie API chat"
else
    bad "bezpośrednie API chat"
fi

echo
echo "[4/6] MFO Web..."
WEB_HEALTH="$(curl -fsS "$WEB/api/health" 2>/dev/null || true)"
if printf '%s' "$WEB_HEALTH" | grep -q '"status":"ok"'; then
    ok "MFO Web /api/health"
else
    bad "MFO Web /api/health"
fi

echo
echo "[5/6] MFO Web chat..."
WEB_CHAT="$(curl -fsS -X POST "$WEB/api/chat" \
  -H 'Content-Type: application/json' \
  -d '{"message":"Reply exactly MFO_WEB_OK"}' 2>/dev/null || true)"

if printf '%s' "$WEB_CHAT" | grep -q 'MFO_WEB_OK'; then
    ok "MFO Web /api/chat"
else
    bad "MFO Web /api/chat"
fi

echo
echo "[6/6] JCODE local_llama — 4 tools..."
JCODE_OUT="$(timeout 180 jcode \
  --provider-profile local_llama \
  --tool-profile lite \
  --tools bash,read,write,apply_patch \
  --model "$MODEL" \
  run 'Reply exactly JCODE_LOCAL_OK' 2>&1 || true)"

if printf '%s' "$JCODE_OUT" | grep -q 'JCODE_LOCAL_OK'; then
    ok "JCODE → local_llama"
else
    bad "JCODE → local_llama"
    echo
    echo "--- wynik JCODE ---"
    printf '%s\n' "$JCODE_OUT" | tail -30
fi

echo
echo "===================================="
echo " PODSUMOWANIE"
echo " PASS: $PASS"
echo " FAIL: $FAIL"
echo "===================================="

if [ "$FAIL" -eq 0 ]; then
    echo "🚀 MFO v6.0 CORE: GOTOWE"
    exit 0
else
    echo "⚠️ MFO wymaga poprawki."
    exit 1
fi
