from adk.base_agent import BaseAgent
from adk.observability import Logger
from adk.a2a_protocol import Message
from adk.context_engineering import EVALUATOR_CONTEXT
import json

class Evaluator(BaseAgent):
    def __init__(self):
        super().__init__(name="Evaluator", context=EVALUATOR_CONTEXT)

    def process(self, message: Message, api_key: str = None) -> dict:
        Logger.log(f"{self.name} auditing draft...")
        draft_budget = message.data.get("draft")
        
        prompt = f"""
        System: {self.context}
        Task: Audit the following draft budget.
        Draft Budget: {json.dumps(draft_budget)}
        
        Output a JSON object with two keys: 'status' ("approved" or "adjusted") and 'final_budget' (a dictionary mapping categories to numbers).
        """
        
        response_text = self.llm.generate(prompt, api_key=api_key, require_json=True)
        try:
            result = json.loads(response_text)
            if 'final_budget' not in result:
                result['final_budget'] = draft_budget
        except:
            result = {"status": "fallback_approved", "final_budget": draft_budget}
            
        return result
