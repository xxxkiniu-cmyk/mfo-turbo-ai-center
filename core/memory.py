import json, pathlib, time
from core.logger import logger
class AgentMemory:
    def __init__(self, agent_name="TestAgent", max_history=5):
        self.agent_name = agent_name
        self.max_history = max_history
        self.file = pathlib.Path(f"storage/memory/{agent_name}_memory.json")
        self.file.parent.mkdir(parents=True, exist_ok=True)
        if not self.file.exists():
            self.file.write_text("[]", encoding="utf-8")
    def remember(self, role_or_user, content):
        try:
            hist = self.get_history()
            hist.append({"role": str(role_or_user), "content": str(content), "time": time.time(), "agent": self.agent_name})
            hist = hist[-self.max_history:]
            self.file.write_text(json.dumps(hist, indent=2, ensure_ascii=False), encoding="utf-8")
            return True
        except: return False
    def get_history(self):
        try:
            if not self.file.exists(): return []
            return json.loads(self.file.read_text(encoding="utf-8"))
        except: return []
    def clear(self):
        try: self.file.write_text("[]", encoding="utf-8")
        except: pass
def test_memory():
    mem = AgentMemory("TestAgent", 5)
    mem.clear()
    mem.remember("test_user", "100%")
    hist = mem.get_history()
    return len(hist)>0 and hist[-1].get("content")=="100%"
