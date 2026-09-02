import datetime, pathlib, uuid
LOG_DIR = pathlib.Path("logs")
LOG_DIR.mkdir(exist_ok=True)
class Logger:
 def __init__(self, name="MFO"):
  self.name=name
 def _log(self, level, msg, context=None, correlation_id=None):
  cid=correlation_id or f"trace_{uuid.uuid4().hex[:8]}"
  ts=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  line=f"[{ts}] [{level}] {msg}"
  print(line)
  try:
   with open(LOG_DIR / f"{datetime.date.today()}.log", "a", encoding="utf-8") as f:
    f.write(line + "\n")
  except: pass
 def info(self, msg, context=None, correlation_id=None):
  self._log("INFO", msg, context, correlation_id)
 def error(self, msg, context=None, correlation_id=None):
  self._log("ERROR", msg, context, correlation_id)
 def warn(self, msg, context=None, correlation_id=None):
  self._log("WARN", msg, context, correlation_id)
logger=Logger()
