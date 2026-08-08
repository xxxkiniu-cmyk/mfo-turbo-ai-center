from agents.base_agent import BaseAgent
from core.memory import AgentMemory
from core.logger import logger
import json, urllib.request

def call_luna_engine(prompt):
    url = "http://127.0.0.1:8080/v1/chat/completions"
    system = "Jestes Luna - ciepla osobowosc i silnik wykonawczy MFO TURBO v2.8. Odpowiadaj ZAWSZE po polsku, krotko, konkretnie. Jestes sercem Turbo."
    payload = {
        "model": "local",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": str(prompt)}
        ],
        "temperature": 0.7,
        "max_tokens": 350
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type":"application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            j = json.loads(r.read().decode())
            return j["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"Luna engine blad: {e}")
        return None

class LunaAgent(BaseAgent):
    def __init__(self, name="LUNA"):
        super().__init__(name=name)
        self.memory = AgentMemory(name, 30)
        logger.info("LunaAgent v2.8 SILNIK gotowy - bezposrednio na 8080")

    def route(self, task):
        try:
            self.memory.remember("user", str(task))
            ans = call_luna_engine(str(task))
            if not ans:
                raise Exception("Silnik Llama offline")
            self.memory.remember("model", ans)
            return ans
        except Exception as e:
            fallback = f"Luna [SILNIK v2.8 OFFLINE]: Ogarnelam - {task}"
            self.memory.remember("model", fallback)
            return fallback

LunaAgent = LunaAgent
