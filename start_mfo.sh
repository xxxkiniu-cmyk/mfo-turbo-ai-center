#!/bin/bash
pkill -9 -f llama-server; pkill -f mfo_web; sleep 1
/usr/local/bin/llama-server -m ~/mfo-models/Llama-3.2-3B-Q4_K_M.gguf -c 512 -t 2 --host 127.0.0.1 --port 1234 > ~/mfo/mfo-turbo-ai-center/llm.log 2>&1 &
sleep 2
cd ~/mfo/mfo-turbo-ai-center && nohup python3 mfo_web.py > web.log 2>&1 &
echo "GOTOWE v5.3 c=512 history=4 timeout 90s"
