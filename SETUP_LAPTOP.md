# SETUP LAPTOP — MFO.ai + JCODE

## Wymagania wstępne
- System Linux z zainstalowanym pakietem `python3` oraz `curl`.
- Lokalny serwer `llama-server` uruchomiony na porcie `1234`.

## Uruchomienie modelu (llama-server)
```bash
llama-server -m /home/xxxkiniu/mfo-models/Qwen2.5-Coder-3B-Instruct-Q4_K_M.gguf --port 1234
