from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
LLM_URL = "http://127.0.0.1:1234/v1/chat/completions"
SYSTEM = "Jestes Luna, koderka MFO TURBO, odpowiadaj krotko po polsku. Twój szef to Krzysztof Mazurkiewicz (Master Home Finish Szczecin)."

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        msg = request.get_json(force=True).get("message","")
        if "kim ja jestem" in msg.lower():
            return jsonify({"response": "Jesteś Krzysztof Mazurkiewicz, Master Home Finish Szczecin."})
        
        payload = {
            "messages": [
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": msg}
            ],
            "temperature": 0.2,
            "max_tokens": 600
        }
        r = requests.post(LLM_URL, json=payload, timeout=180)
        txt = r.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        return jsonify({"response": txt.strip()})
    except Exception as e:
        return jsonify({"response": f"Blad komunikacji LLM: {e}"}), 500

@app.route("/")
def idx():
    try: return open("chat.html", encoding="utf-8").read()
    except: return "<h1>MFO TURBO READY - POST /api/chat</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8082)
