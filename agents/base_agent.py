from core.logger import logger
class BaseAgent:
 def __init__(self, name):
  self.name=name
  logger.info(f"Agent {name} gotowy")
 def run(self, task):
  logger.info(f"[{self.name}] Wykonuje: {task}")
  return {"agent":self.name,"task":task,"status":"OK"}
