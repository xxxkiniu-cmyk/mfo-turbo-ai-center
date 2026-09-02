from flask import Flask, request, jsonify
import requests
app = Flask(__name__)
LLM_URL = "http://127.0.0.1:1234/completion"
SYSTEM = "Jestes Luna, koderka MFO TURBO, odpowiadaj po polsku. Szef Krzysztof Mazurkiewicz MFO Szczecin."
@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        msg = request.get_json(force=True).get("message","")
        if "kim ja jestem" in msg.lower():
            return jsonify({"response": "Jestes Krzysztof Mazurkiewicz, Master Home Finish Szczecin."})
        prompt = f"<|im_start|>system\n{SYSTEM}<|im_end|>\n<|im_start|>user\n{msg}<|im_end|>\n<|im_start|>assistant\n"
        r = requests.post(LLM_URL, json={"prompt": prompt, "n_predict": 600, "temperature": 0.2, "stop": ["<|im_end|>"]}, timeout=180)
        txt = r.json().get("content") or r.json().get("completion") or ""
        return jsonify({"response": txt})
    except Exception as e:
        return jsonify({"response": f"Blad: {e}. Sprawdz czy 8081 dziala."}), 500
@app.route("/")
def idx():
    try: return open("chat.html", encoding="utf-8").read()
    except: return "<h1>MFO TURBO READY - POST /api/chat</h1>"
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8082)
