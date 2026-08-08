from .base_agent import BaseAgent
class RouterAgent(BaseAgent):
 def __init__(self):
  super().__init__("ROUTER")
 def route(self, msg):
  return self.run(f"Routuje: {msg}")
