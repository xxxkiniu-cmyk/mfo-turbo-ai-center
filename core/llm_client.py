from .secrets import GEMINI_API_KEY
from .logger import logger
from .config import load_config
class LLMClient:
 def __init__(self):
  self.config=load_config()
 def chat(self, prompt, model="gemini-2.5-flash"):
  if not GEMINI_API_KEY:
   logger.warn("Brak klucza - zwracam mock offline")
   return {"project_name":"MFO TURBO AI CENTER","mock":True}
  logger.info(f"Wybrany model AI: {model}")
  return {"project_name":"MFO TURBO AI CENTER","model":model,"ok":True}
client=LLMClient()
