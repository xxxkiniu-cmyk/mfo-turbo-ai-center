import pathlib
print("=== DIAGNOZA TRYTYTKOWA ===")
for p in ["core/__init__.py","core/config.py","core/event_bus.py","core/secrets.py","core/logger.py","core/llm_client.py","core/ai_router.py","agents/base_agent.py","agents/router_agent.py","utils/helpers.py","settings.json","main.py",".env"]:
 path=pathlib.Path(p)
 status="✅" if path.exists() else "❌ BRAK"
 size=path.stat().st_size if path.exists() else 0
 print(f"{status} {p} ({size}B)")
print("=== KONIEC DIAGNOZY ===")
