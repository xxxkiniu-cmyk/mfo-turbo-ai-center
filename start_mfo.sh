#!/bin/bash
cd ~/mfo/mfo-turbo-ai-center/
pkill -f llama-server
pkill -f mfo_web.py
if [ -f "$HOME/mfo/llama.cpp/build/bin/llama-server" ]; then
    LLAMA="$HOME/mfo/llama.cpp/build/bin/llama-server"
elif [ -f "$HOME/.mfo/llama.cpp/build/bin/llama-server" ]; then
    LLAMA="$HOME/.mfo/llama.cpp/build/bin/llama-server"
else
    LLAMA="llama-server"
fi
MODEL="$HOME/mfo/llama.cpp/models/Llama-3.2-3B-Q4_K_M.gguf"
[ ! -f "$MODEL" ] && MODEL="$HOME/mfo-models/Llama-3.2-3B-Q4_K_M.gguf"
echo "LLAMA: $LLAMA"
echo "MODEL: $MODEL"
nohup $LLAMA -m "$MODEL" --port 1234 --host 0.0.0.0 -c 2048 --repeat-penalty 1.1 --temp 0.7 > llm.log 2>&1 &
sleep 3
nohup python3 mfo_web.py > web.log 2>&1 &
echo "OK WEB: http://127.0.0.1:8082"
echo "OK API: http://127.0.0.1:1234"
