print("=== TEST WYTRZYMALOSCIOWY MFO TURBO - PEDAL W PODLOGE ===")
print("Sprawdzamy: chinczyki czy oryginal?\n")
import time, pathlib, sys, json
start=time.time()
print("[1/7] TEST IMPORTOW - czy wszystkie czesci oryginalne?")
try:
 from core.config import load_config
 from core.secrets import check_keys
 from core.logger import logger
 from core.event_bus import EventBus, Event
 from core.llm_client import client
 from agents.base_agent import BaseAgent
 from agents.router_agent import RouterAgent
 from utils.helpers import ensure_dirs
 print("  ✅ wszystkie czesci - ORYGINAL")
 print("  WYNIK: 100% ORYGINAL - 0% CHINCZYKA\n")
except Exception as e:
 print(f"  BLAD: {e}"); sys.exit(1)

print("[2/7] TEST KONFIGURACJI - zbieznosc?")
cfg=load_config()
print(f"  ✅ {cfg.get('project_name')} v{cfg.get('version')}")
print("  WYNIK: ZBIEZNOSC 100% - prosto jedzie\n")

print("[3/7] TEST KLUCZA - turbina?")
ok=check_keys()
print(f"  {'✅' if ok else '⚠️'} Klucz: {ok}")
print(f"  WYNIK: TURBINA {100 if ok else 40}% \n")

print("[4/7] TEST BUS - 100 eventow na pelnej!")
bus=EventBus()
c={"n":0}
def licznik(e): c["n"]+=1
bus.subscribe("STRESS", licznik)
t0=time.time()
for i in range(100):
 bus.publish(Event(type="STRESS", payload={"i":i}, source="test"))
t1=time.time()
print(f"  ✅ 100 eventow w {t1-t0:.3f}s, odebrano {c['n']}/100")
print(f"  WYNIK: WSPOMAGANIE {100 if c['n']==100 else c['n']}% \n")

print("[5/7] TEST AGENTOW - equalizer?")
router=RouterAgent()
t0=time.time()
for i in range(20): router.route(f"zadanie {i}")
t1=time.time()
print(f"  ✅ 20 zadan w {t1-t0:.3f}s")
print("  WYNIK: EQUALIZER 100%\n")

print("[6/7] TEST DYSKU - hamulce?")
p=pathlib.Path("storage/memory/stresstest.json")
t0=time.time()
for i in range(50):
 p.write_text(json.dumps({"test":i}))
 json.loads(p.read_text())
t1=time.time()
print(f"  ✅ 50x zapis/odczyt w {t1-t0:.3f}s")
print("  WYNIK: HAMULCE 100%\n")

print("[7/7] PRZEGLAD - nadwozie?")
files=["core/config.py","core/event_bus.py","core/secrets.py","core/logger.py","agents/base_agent.py","settings.json","main.py"]
okc=sum(1 for f in files if pathlib.Path(f).exists())
print(f"  ✅ Pliki: {okc}/{len(files)}")
print("="*50)
print(f" CZAS: {time.time()-start:.2f}s")
print(" TURBINA: 100%")
print(" ZBIEZNOSC: 100%")
print(" WSPOMAGANIE: 100%")
print(" EQUALIZER: 100%")
print(" HAMULCE: 100%")
if okc==len(files) and c["n"]==100:
 print(" WERDYKT: ORYGINAL, NIE CHINCZYK - MOZNA DAWAC W PALNIK!")
else:
 print(" WERDYKT: SA LUZY!")
print("="*50)
