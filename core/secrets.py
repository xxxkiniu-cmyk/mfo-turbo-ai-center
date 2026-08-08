import os, pathlib
def load_dotenv():
 p=pathlib.Path(".env")
 if not p.exists(): return
 for line in p.read_text(encoding="utf-8").splitlines():
  line=line.strip()
  if not line or line.startswith("#") or "=" not in line: continue
  k,v=line.split("=",1)
  os.environ[k.strip()]=v.strip().strip('"').strip("'")
load_dotenv()
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY","")
def check_keys():
 ok=len(GEMINI_API_KEY)>20
 print(f"[{'INFO' if ok else 'ERROR'}] Klucz API {'jest poprawnie skonfigurowany.' if ok else 'BRAK KLUCZA w .env'}")
 return ok
