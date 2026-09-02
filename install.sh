#!/bin/bash
cd ~/.mfo/mfo-turbo-ai-center/
cp conversation_history.json conversation_history.json.bak 2>/dev/null
rm -f mfo_web.py web.log index.html

cat > mfo_web.py <<'PY'
import json,os,threading
import urllib.request
from http.server import BaseHTTPRequestHandler as H
from http.server import HTTPServer

HIST="conversation_history.json"
LLM="http://127.0.0.1:8081/completion"
LOCK=threading.Lock()
SYS="Jestes Luna. Twoje imie to Luna. "
SYS+="Uzytkownik to Krzysiek, mow do niego Krzychu."

def load_h():
    if not os.path.exists(HIST):
        return [{"role":"system","content":SYS}]
    try:
        with open(HIST,"r",encoding="utf-8") as f:
            return json.load(f)
    except:
        return [{"role":"system","content":SYS}]

def save_h(h):
    with open(HIST,"w",encoding="utf-8") as f:
        json.dump(h,f,ensure_ascii=False,indent=2)

def build_prompt(h):
    out=""
    for m in h[-10:]:
        r=m.get("role","")
        c=m.get("content","")
        if r=="system":
            out+=f"System: {c}\n"
        elif r=="user":
            out+=f"Krzychu: {c}\n"
        else:
            out+=f"Luna: {c}\n"
    out+="Luna:"
    return out

def ask_llm(prompt):
    data={
        "prompt":prompt,
        "temperature":0.2,
        "n_predict":280,
        "stop":["Krzychu:","System:"]
    }
    req=urllib.request.Request(
        LLM,
        data=json.dumps(data).encode(),
        headers={"Content-Type":"application/json"}
    )
    with urllib.request.urlopen(req,timeout=60) as r:
        j=json.loads(r.read().decode())
        return j.get("content","").strip()

class Handler(H):
    def do_GET(self):
        if self.path=="/" or self.path=="/index.html":
            self.send_response(200)
            self.send_header("Content-type","text/html")
            self.end_headers()
            with open("index.html","rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path!="/api/chat":
            self.send_response(404)
            self.end_headers()
            return
        ln=int(self.headers.get("Content-Length",0))
        body=self.rfile.read(ln).decode()
        um=json.loads(body).get("message","")
        with LOCK:
            h=load_h()
            h.append({"role":"user","content":um})
            prompt=build_prompt(h)
            ans=ask_llm(prompt)
            h.append({"role":"assistant","content":ans})
            if len(h)>23:
                h=[h[0]]+h[-22:]
            save_h(h)
        self.send_response(200)
        self.send_header("Content-type","application/json")
        self.end_headers()
        self.wfile.write(
            json.dumps(
                {"reply":ans},
                ensure_ascii=False
            ).encode()
        )

if __name__=="__main__":
    srv=HTTPServer(("127.0.0.1",8082),Handler)
    print("WEB 8082 -> LLM 8081")
    srv.serve_forever()
PY

cat > index.html <<'HTML'
<!doctype html>
<html><head>
<meta charset="utf-8">
<meta name="viewport"
 content="width=device-width,initial-scale=1">
<title>Luna - MFO</title>
<style>
body{margin:0;font-family:sans-serif;
 background:#111;color:#eee;display:flex;
 flex-direction:column;height:100vh}
#chat{flex:1;overflow-y:auto;padding:10px}
.msg{margin:6px 0;padding:8px 10px;
 border-radius:8px;max-width:85%}
.user{background:#2a5bd7;margin-left:auto}
.bot{background:#222}
#bar{display:flex;padding:8px;background:#000}
#inp{flex:1;padding:10px;border-radius:6px;
 border:none;background:#222;color:#fff}
#btn{margin-left:6px;padding:10px 14px;
 border:none;border-radius:6px;
 background:#2a5bd7;color:#fff}
</style></head><body>
<div id="chat"></div>
<div id="bar">
<input id="inp" placeholder="Napisz do Luny...">
<button id="btn">Wyslij</button>
</div>
<script>
const chat=document.getElementById('chat');
const inp=document.getElementById('inp');
const btn=document.getElementById('btn');
function add(t,cls){
 const d=document.createElement('div');
 d.className='msg '+cls;
 d.textContent=t;
 chat.appendChild(d);
 chat.scrollTop=chat.scrollHeight;
}
async function send(){
 const m=inp.value.trim();
 if(!m)return;
 add(m,'user');
 inp.value='';
 const r=await fetch('/api/chat',{
   method:'POST',
   headers:{'Content-Type':'application/json'},
   body:JSON.stringify({message:m})
 });
 const j=await r.json();
 add(j.reply,'bot');
}
btn.onclick=send;
inp.onkeydown=e=>{
 if(e.key==='Enter')send();
};
</script></body></html>
HTML

python -m py_compile mfo_web.py && echo "OK skompilowane"
ls -lh mfo_web.py index.html

