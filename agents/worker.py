from project.adk.base_agent import BaseAgent
from project.adk.observability import Logger
from project.adk.a2a_protocol import Message
from project.adk.context_engineering import WORKER_CONTEXT
from project.skills.calculator_skill import CalculatorSkill

class Worker(BaseAgent):
    def __init__(self):
        super().__init__(name="Worker", context=WORKER_CONTEXT)
        self.equip_skill(CalculatorSkill())

    def process(self, message: Message) -> Message:
        Logger.log(f"{self.name} received task: {message.task}")
        food_calc = self.execute_skill("calculator", expression="150 + 250")
        draft_budget = {"Housing": 1200, "Food": food_calc, "Savings": 500}
        return Message(sender=self.name, receiver="Evaluator", task="audit_budget", data={"draft": draft_budget})
