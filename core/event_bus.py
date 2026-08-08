import json, pathlib, uuid, datetime
from collections import defaultdict
class Event:
 def __init__(self, type, payload, source="main", correlation_id=None):
  self.type=type; self.payload=payload; self.source=source
  self.timestamp=datetime.datetime.now().isoformat()
  self.correlation_id=correlation_id or f"trace_{uuid.uuid4().hex[:8]}"
 def to_dict(self):
  return {"type":self.type,"payload":self.payload,"source":self.source,"timestamp":self.timestamp,"correlation_id":self.correlation_id}
class EventBus:
 def __init__(self):
  self._subs=defaultdict(list)
  self._log=[]
 def subscribe(self, et, cb):
  self._subs[et].append(cb)
 def publish(self, event):
  self._log.append(event.to_dict())
  for cb in self._subs.get(event.type,[]):
   try: cb(event)
   except Exception as e: print(f"[BUS ERROR] {e}")
  try:
   pathlib.Path("storage/events").mkdir(parents=True, exist_ok=True)
   with open(f"storage/events/{event.correlation_id}.json","w",encoding="utf-8") as f:
    json.dump(event.to_dict(), f, ensure_ascii=False, indent=2)
  except: pass
  return event.correlation_id
BUS=EventBus()
