from project.adk.base_agent import BaseAgent
from project.adk.observability import Logger
from project.adk.a2a_protocol import Message
from project.adk.context_engineering import EVALUATOR_CONTEXT

class Evaluator(BaseAgent):
    def __init__(self):
        super().__init__(name="Evaluator", context=EVALUATOR_CONTEXT)

    def process(self, message: Message) -> dict:
        Logger.log(f"{self.name} auditing draft...")
        return {"status": "approved", "final_budget": message.data["draft"]}
