import json,os,requests
HF=os.path.expanduser("~/.mfo/mfo-turbo-ai-center/conversation_history.json")
URL="http://127.0.0.1:8081/v1/chat/completions"
SYS="Jestes Luna. Twoje imie to Luna. Uzytkownik to Krzysiek, mow do niego Krzychu. Pamietaj to zawsze."
def load():
 try: return json.load(open(HF,encoding="utf-8"))
 except: return [{"role":"system","content":SYS},{"role":"user","content":"Mam na imie Krzysiek"},{"role":"assistant","content":"Hej Krzychu!"}]
def save(h): open(HF,"w",encoding="utf-8").write(json.dumps(h,ensure_ascii=False,indent=2))
h=load()
print(f"[SYSTEM] v6 Luna 512 STABLE, {len(h)} wiad.")
while True:
 q=input("TY> ")
 if not q.strip(): continue
 if q.lower() in ["koniec","q"]: break
 h.append({"role":"user","content":q})
 msgs=[h[0]]+h[-4:]
 try:
  r=requests.post(URL,json={"model":"model","messages":msgs,"max_tokens":200,"temperature":0.2,"stop":["<|im_end|>"]},timeout=90)
  a=r.json()["choices"][0]["message"]["content"]
  print(f"\nLUNA: {a}\n")
  h.append({"role":"assistant","content":a}); save(h)
 except Exception as e:
  print(f"[BLAD] {e}"); h.pop()
