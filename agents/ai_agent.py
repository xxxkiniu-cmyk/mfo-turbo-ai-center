from agents.base_agent import BaseAgent
from core.memory import AgentMemory
from core.logger import logger
import json, urllib.request

class AIAgent(BaseAgent):
    def __init__(self, name="AI_AGENT"):
        super().__init__(name=name)
        self.memory = AgentMemory(name, 20)
        self.url = "http://127.0.0.1:8080/completion"
        logger.info("AIAgent LOCAL TURBO - llama.cpp")

    def _call_local(self, prompt, hist):
        # bierzemy ostatnie 4 wiadomości z pamięci
        context = ""
        for h in hist[-4:]:
            context += f"{h.get('role')}: {h.get('content')}\n"
        full_prompt = f"{context}\nuser: {prompt}\nassistant:"

        data = json.dumps({
            "prompt": full_prompt,
            "n_predict": 512,
            "temperature": 0.7,
            "stop": ["user:", "###"]
        }).encode()
        req = urllib.request.Request(self.url, data=data, headers={"Content-Type":"application/json"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                j = json.loads(r.read().decode())
                return j.get("content","").strip()
        except Exception as e:
            logger.error(f"LOCAL LLM blad: {e}")
            return None

    def route(self, task):
        try:
            self.memory.remember("user", str(task))
            ans = self._call_local(str(task), self.memory.get_history())
            if not ans:
                raise Exception("Serwer llama.cpp nie odpowiada")
            self.memory.remember("model", ans)
            return ans
        except Exception as e:
            print(f"⚠️ Turbina lokalna niedostepna ({e}). Tryb awaryjny.")
            fb = f"AI_AGENT ogarnal: {task} [OFFLINE]"
            self.memory.remember("model", fb)
            return fb

AiAgent = AIAgent
