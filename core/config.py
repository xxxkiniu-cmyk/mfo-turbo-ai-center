import json, pathlib
def load_config():
 cfg={"project_name":"MFO TURBO AI CENTER","version":"2.4","offline":True}
 for p in [pathlib.Path("settings.json"), pathlib.Path("config/settings.json"), pathlib.Path("config/config.json")]:
  if p.exists():
   try:
    data=json.loads(p.read_text(encoding="utf-8"))
    cfg.update(data)
    print(f"[INFO] Konfiguracja z {p} zostala pomyslnie wczytana.")
    return cfg
   except Exception as e:
    print(f"[WARN] Blad {p}: {e}")
 if pathlib.Path(".env").exists():
  print("[INFO] Konfiguracja z .env (fallback)")
 return cfg
