from adk.base_agent import BaseAgent
from adk.observability import Logger
from adk.a2a_protocol import Message
from adk.context_engineering import WORKER_CONTEXT
from skills.calculator_skill import CalculatorSkill
import json

class Worker(BaseAgent):
    def __init__(self):
        super().__init__(name="Worker", context=WORKER_CONTEXT)
        self.equip_skill(CalculatorSkill())

    def process(self, message: Message, api_key: str = None) -> Message:
        Logger.log(f"{self.name} received task: {message.task}")
        
        prompt = f"""
        System: {self.context}
        Task: Draft a budget based on the following strategy.
        Strategy: {message.data.get('strategy')}
        User Input: {message.data.get('input')}
        
        Output a JSON object mapping budget categories (e.g., 'Housing', 'Food', 'Savings') to numeric dollar amounts.
        """
        
        response_text = self.llm.generate(prompt, api_key=api_key, require_json=True)
        try:
            draft_budget = json.loads(response_text)
        except:
            food_calc = self.execute_skill("calculator", expression="150 + 250")
            draft_budget = {"Housing": 1200, "Food": food_calc, "Savings": 500}
            
        return Message(sender=self.name, receiver="Evaluator", task="audit_budget", data={"draft": draft_budget})
