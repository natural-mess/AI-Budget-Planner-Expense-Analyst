from project.adk.base_agent import BaseAgent
from project.adk.observability import Logger
from project.adk.a2a_protocol import Message
from project.adk.context_engineering import PLANNER_CONTEXT

class Planner(BaseAgent):
    def __init__(self):
        super().__init__(name="Planner", context=PLANNER_CONTEXT)

    def process(self, user_input: str) -> Message:
        Logger.log(f"{self.name} processing input: '{user_input}'")
        return Message(sender=self.name, receiver="Worker", task="draft_budget", data={"input": user_input, "strategy": "50/30/20"})
