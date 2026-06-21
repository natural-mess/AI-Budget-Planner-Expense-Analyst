from adk.base_agent import BaseAgent
from adk.observability import Logger
from adk.a2a_protocol import Message
from adk.context_engineering import PLANNER_CONTEXT
import json

class Planner(BaseAgent):
    def __init__(self):
        super().__init__(name="Planner", context=PLANNER_CONTEXT)

    def process(self, user_input: str, api_key: str = None) -> Message:
        Logger.log(f"{self.name} processing input: '{user_input}'")
        
        prompt = f"""
        System: {self.context}
        User Request: {user_input}
        
        Output a JSON object with a single key 'strategy' detailing your high-level financial plan.
        """
        
        response_text = self.llm.generate(prompt, api_key=api_key, require_json=True)
        try:
            strategy_data = json.loads(response_text)
            strategy = strategy_data.get("strategy", "Default Strategy")
        except:
            strategy = "Fallback Strategy due to JSON parsing error."
            
        return Message(sender=self.name, receiver="Worker", task="draft_budget", data={"input": user_input, "strategy": strategy})
