from agents.planner import Planner
from agents.worker import Worker
from agents.evaluator import Evaluator
from memory.session_memory import SessionMemory
from adk.observability import Logger
from adk.security_manager import SecurityManager
from skills.pii_redactor_skill import PIIRedactorSkill

class MainAgent:
    def __init__(self):
        self.planner = Planner()
        self.worker = Worker()
        self.evaluator = Evaluator()
        self.memory = SessionMemory()
        self.pii_skill = PIIRedactorSkill()

    def handle_message(self, user_input: str, api_key: str = None) -> dict:
        safe_input = self.pii_skill.execute(text=user_input)
        if safe_input != user_input:
            Logger.log("MainAgent: PII redacted from user input.")

        self.memory.add({"role": "user", "content": safe_input})
        Logger.log("MainAgent initialized workflow.")
        
        plan_msg = self.planner.process(safe_input, api_key)
        worker_msg = self.worker.process(plan_msg, api_key)
        eval_result = self.evaluator.process(worker_msg, api_key)
        
        final_budget = eval_result['final_budget']
        
        needs_approval = SecurityManager.require_hitl_approval(final_budget)
        
        if needs_approval:
            return {"status": "awaiting_approval", "budget": final_budget}
        else:
            response = f"Final Budget: {final_budget}"
            self.memory.add({"role": "system", "content": response})
            return {"status": "complete", "response": response, "budget": final_budget}

    def approve_budget(self, budget: dict) -> dict:
        response = f"Final Budget (Approved): {budget}"
        self.memory.add({"role": "system", "content": response})
        return {"status": "complete", "response": response, "budget": budget}

def run_agent(user_input: str):
    agent = MainAgent()
    result = agent.handle_message(user_input)
    if result["status"] == "awaiting_approval":
        result = agent.approve_budget(result["budget"])
    return result["response"]
