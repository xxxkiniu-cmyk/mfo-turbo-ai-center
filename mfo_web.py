from flask import Flask, request, jsonify, send_from_directory
import requests, pathlib
app = Flask(__name__)
LLM_API = "http://127.0.0.1:1234/v1/chat/completions"
BASE = pathlib.Path.home() / "mfo" / "mfo-turbo-ai-center"
def tool_list():
    files=[x.name for x in sorted(BASE.iterdir()) if x.is_file() and not x.name.startswith(".") and x.suffix!=".log"]
    return sorted(set(files))
history=[]
@app.route("/")
def index():
    return send_from_directory(str(BASE),"chat.html")
@app.route("/api/chat",methods=["POST"])
def chat():
    global history
    msg=request.json.get("message","").strip()
    if not msg: return jsonify({"reply":"?","response":"?"})
    low=msg.lower()
    if any(k in low for k in ["folder","pliki","co masz","lista","zawartosc"]):
        files=tool_list()
        txt="Pliki na dysku (100% fakty):\n- " + "\n- ".join(files[:20])
        history.append({"role":"user","content":msg})
        history.append({"role":"assistant","content":txt})
        history=history[-10:]
        return jsonify({"reply":txt,"response":txt})
    system_msg = "Jestes pomocna asystentka LUNA. Pamietasz imie uzytkownika i fakty. Gdy pytaja 'jak mam na imie' odpowiadasz imieniem uzytkownika, nie swoim. Krotko po polsku."
    # SMART: dlugie wiadomosci = mniej historii = szybsze
    hist_len = 4 if len(msg) > 80 else 10
    msgs=[{"role":"system","content":system_msg}]+history[-hist_len:]+[{"role":"user","content":msg}]
    try:
        r=requests.post(LLM_API,json={"model":"Llama-3.2-3B","messages":msgs,"temperature":0.0,"max_tokens":80},timeout=120)
        ai=r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        ai=f"BLAD {e}"
    history.append({"role":"user","content":msg})
    history.append({"role":"assistant","content":ai})
    history=history[-10:]
    return jsonify({"reply":ai,"response":ai})
@app.route("/api/status")
def status():
    return jsonify({"status":"LUNA v5.5 SMART FIX","c":512,"history":len(history),"fix":"smart history 4/10 + timeout 120s"})
if __name__=="__main__":
    app.run(host="127.0.0.1",port=8082)
