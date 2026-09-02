import pathlib
from core.logger import logger

def ensure_dirs():
    for d in ["logs","storage/events","storage/memory","agents","utils","config"]:
        pathlib.Path(d).mkdir(parents=True, exist_ok=True)

def clean_old_traces(max_files=20):
    events_dir = pathlib.Path("storage/events")
    if not events_dir.exists():
        return 0
    files = sorted(events_dir.glob("trace_*.json"), key=lambda p: p.stat().st_mtime)
    if len(files) > max_files:
        to_delete = files[:-max_files]
        for f in to_delete:
            try:
                f.unlink()
            except:
                pass
        logger.info(f"Posprzatano {len(to_delete)} starych trace")
        return len(to_delete)
    return 0

def system_check():
    return {"ok": True}
