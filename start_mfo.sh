#!/bin/bash
pkill -9 -f llama-server; pkill -f mfo_web; sleep 1
rm -f ~/mfo/mfo-turbo-ai-center/llm.log ~/mfo/mfo-turbo-ai-center/web.log
LD_LIBRARY_PATH=/opt/llama /opt/llama/llama-server -m ~/mfo-models/Qwen2.5-Coder-3B-Instruct-Q4_K_M.gguf -c 4096 -t 4 --threads-batch 4 --flash-attn on --batch-size 512 --host 127.0.0.1 --port 1234 --jinja -np 1 --cache-type-k q8_0 --cache-type-v q8_0 > ~/mfo/mfo-turbo-ai-center/llm.log 2>&1 &
echo -n "Czekam na model"
for i in {1..60}; do
  curl -s http://127.0.0.1:1234/v1/models | grep -q "object" && break
  echo -n "."
  sleep 1
done
echo ""
cd ~/mfo/mfo-turbo-ai-center && nohup python3 mfo_web.py > web.log 2>&1 &
echo "GOTOWE v5.9"
