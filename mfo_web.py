from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

LLAMA_BASE = "http://127.0.0.1:1234"
LLAMA_CHAT_URL = f"{LLAMA_BASE}/v1/chat/completions"
MODEL = "/home/xxxkiniu/mfo-models/Qwen2.5-Coder-3B-Instruct-Q4_K_M.gguf"

SYSTEM_PROMPT = (
    "Jestes ekspertem Python. Pisz kompletny, dzialajacy kod. "
    "Nie skracaj odpowiedzi i nie zastepuj kodu opisem typu 'to jest algorytm'. "
    "Zawsze zwracaj pelny kod w bloku ```python. "
    "Jesli zadanie wymaga testu lub przykladu uruchomienia, dolacz go w calosci."
)

@app.get("/api/health")
def health():
    try:
        r = requests.get(f"{LLAMA_BASE}/v1/models", timeout=3)
        r.raise_for_status()
        return jsonify({
            "status": "ok",
            "llama": LLAMA_BASE,
            "llama_ready": True,
            "models": r.json(),
        })
    except Exception as exc:
        return jsonify({
            "status": "error",
            "llama": LLAMA_BASE,
            "llama_ready": False,
            "error": str(exc),
        }), 503

@app.post("/api/chat")
def chat():
    body = request.get_json(silent=True) or {}
    user_msg = body.get("message") or body.get("prompt") or ""

    if not isinstance(user_msg, str) or not user_msg.strip():
        return jsonify({"error": "Brak pola 'message' lub 'prompt'."}), 400

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg.strip()},
        ],
        "temperature": 0.4,
        "top_p": 0.9,
        "max_tokens": 2048,
        "stream": False,
    }

    try:
        r = requests.post(LLAMA_CHAT_URL, json=payload, timeout=180)
    except requests.RequestException as exc:
        return jsonify({"error": f"Blad polaczenia z llama-server: {exc}"}), 502

    try:
        data = r.json()
    except ValueError:
        return jsonify({
            "error": "llama-server zwrocil odpowiedz nie-JSON",
            "status_code": r.status_code,
            "body": r.text[:2000],
        }), 502

    if not r.ok:
        return jsonify({
            "error": "llama-server zwrocil blad",
            "status_code": r.status_code,
            "upstream": data,
        }), 502

    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        return jsonify({
            "error": "Nieoczekiwany format odpowiedzi llama-server",
            "raw": data,
        }), 502

    return jsonify({"response": content, "raw": data})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8082, debug=False)
