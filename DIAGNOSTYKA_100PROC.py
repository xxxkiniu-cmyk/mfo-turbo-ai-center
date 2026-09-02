import time, pathlib, sys, json
start = time.time()

print("=== STACJA KONTROLI JAKOŚCI MFO TURBO v2.8 ===")
print("Przeprowadzam pełny przegląd całego systemu...\n")

wyniki = {}

# 1. TEST IMPORTÓW (Części i silnik)
print("[1/6] Sprawdzam moduły i części...")
try:
    from core.config import load_config
    from core.secrets import check_keys
    from core.logger import logger
    from core.event_bus import EventBus, Event
    from core.llm_client import client
    from agents.base_agent import BaseAgent
    from agents.router_agent import RouterAgent
    from agents.ai_agent import AiAgent
    from core.memory import AgentMemory
    wyniki["moduly"] = 100
    print("  ✅ Wszystkie moduły na miejscu: 100%")
except Exception as e:
    wyniki["moduly"] = 0
    print(f"  ❌ Błąd modułów: {e}")

# 2. TEST KONFIGURACJI (Zbieżność)
print("[2/6] Sprawdzam zbieżność i ustawienia...")
try:
    cfg = load_config()
    if cfg.get("project_name"):
        wyniki["konfiguracja"] = 100
        print(f"  ✅ Konfiguracja OK ({cfg.get('project_name')}): 100%")
    else:
        wyniki["konfiguracja"] = 50
        print("  ⚠️ Konfiguracja częściowa: 50%")
except Exception:
    wyniki["konfiguracja"] = 0
    print("  ❌ Brak poprawnej konfiguracji: 0%")

# 3. TEST KLUCZA I TURBINY (AI)
print("[3/6] Sprawdzam turbinę (Klucz API)...")
ok_key = check_keys()
if ok_key:
    wyniki["turbina"] = 100
    print("  ✅ Turbina dmucha na 100% (Klucz API OK)")
else:
    wyniki["turbina"] = 40
    print("  ⚠️ Turbina słaba (Brak klucza / Tryb offline): 40%")

# 4. TEST SZYNY ZDARZEŃ (Wspomaganie / EventBus)
print("[4/6] Sprawdzam szynę zdarzeń (EventBus)...")
try:
    bus = EventBus()
    skrzynka = {"licznik": 0}
    bus.subscribe("TEST_DIAG", lambda e: skrzynka.update({"licznik": skrzynka["licznik"] + 1}))
    bus.publish(Event(type="TEST_DIAG", payload={}, source="diag"))
    if skrzynka["licznik"] == 1:
        wyniki["wspomaganie"] = 100
        print("  ✅ Szyna zdarzeń działa płynnie: 100%")
    else:
        wyniki["wspomaganie"] = 50
        print("  ⚠️ Szyna zdarzeń gubi pakiety: 50%")
except Exception:
    wyniki["wspomaganie"] = 0
    print("  ❌ Awaria szyny zdarzeń: 0%")

# 5. TEST PAMIĘCI AGENTÓW (Short-term memory)
print("[5/6] Sprawdzam pamięć krótkotrwałą...")
try:
    mem = AgentMemory("TestAgent", max_history=5)
    mem.remember("test_user", "100%")
    hist = mem.get_history()
    if len(hist) > 0 and hist[-1]["content"] == "100%":
        wyniki["pamiec"] = 100
        print("  ✅ Pamięć agentów zapisuje i odczytuje poprawnie: 100%")
    else:
        wyniki["pamiec"] = 50
        print("  ⚠️ Pamięć ma opory: 50%")
except Exception:
    wyniki["pamiec"] = 0
    print("  ❌ Pamięć nie działa: 0%")

# 6. TEST HAMULCÓW (Dysk i Cleaner)
print("[6/6] Sprawdzam hamulce (Dysk i Cleaner)...")
try:
    test_file = pathlib.Path("storage/memory/diag_test.json")
    test_file.write_text('{"status": "ok"}', encoding="utf-8")
    data = json.loads(test_file.read_text(encoding="utf-8"))
    test_file.unlink(missing_ok=True)
    if data.get("status") == "ok":
        wyniki["hamulce"] = 100
        print("  ✅ Zapis i odczyt dysku bez zacięć: 100%")
    else:
        wyniki["hamulce"] = 50
        print("  ⚠️ Dysk muli: 50%")
except Exception:
    wyniki["hamulce"] = 0
    print("  ❌ Awaria dysku: 0%")

# PODSUMOWANIE PROCENTOWE CAŁOŚCI
czas_trwania = time.time() - start
srednia_sprawnosc = sum(wyniki.values()) / len(wyniki)

print("\n" + "="*50)
print(f" RAPORT KOŃCOWY SPRAWNOŚCI SYSTEMU:")
print(f" Czas przeglądu: {czas_trwania:.2f}s")
print(f" - Moduły i części: {wyniki.get('moduly', 0)}%")
print(f" - Konfiguracja (Zbieżność): {wyniki.get('konfiguracja', 0)}%")
print(f" - Turbina (AI): {wyniki.get('turbina', 0)}%")
print(f" - Wspomaganie (EventBus): {wyniki.get('wspomaganie', 0)}%")
print(f" - Pamięć agentów: {wyniki.get('pamiec', 0)}%")
print(f" - Hamulce (Dysk): {wyniki.get('hamulce', 0)}%")
print("-"*50)
print(f" 🔥 OGÓLNA SPRAWNOŚĆ CAŁOŚCI: {srednia_sprawnosc:.1f}%")
if srednia_sprawnosc >= 95:
    print(" WERDYKT: MASZYNA JEST W IDEALNYM STANIE - ŻADNYCH LUZÓW, MOŻNA DAWAĆ W PALNIK!")
else:
    print(" WERDYKT: WYMAGA DROBNEJ REGULACJI!")
print("="*50)
