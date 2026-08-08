print("=== MFO TURBO v2.6 TURBO + CLEANER ===")
import pathlib
from utils.helpers import ensure_dirs, clean_old_traces
ensure_dirs()
c = clean_old_traces(20)
if c>0:
    print(f"[CLEANER] Posprzatano {c} starych trace")

try:
    from core.config import load_config
    from core.secrets import check_keys
    from core.logger import logger
    from core.event_bus import EventBus, Event
    from agents.router_agent import RouterAgent
    cfg=load_config()
    logger.info(f"Projekt: {cfg.get('project_name')} v{cfg.get('version')}")
    if not check_keys():
        logger.warn("Brak klucza - OFFLINE")
    else:
        logger.info("Klucz API OK")
        from core.llm_client import client
    bus=EventBus()
    router=RouterAgent()
    def on_test(e):
        print(f"[BUS] {e.type} OK!")
        clean_old_traces(20)
    bus.subscribe("TEST", on_test)
    bus.publish(Event(type="TEST", payload={"msg":"cleaner"}, source="main"))
    router.route("Test z cleanerem")
    print("="*50)
    print(" POSPRZATANE - max 20 trace")
    print(" Agent nie wywali systemu")
    print("="*50)
except Exception as e:
    import traceback
    print(f"BLAD: {e}")
    traceback.print_exc()
