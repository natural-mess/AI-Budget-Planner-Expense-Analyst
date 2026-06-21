from project.agents.planner import Planner
from project.agents.worker import Worker
from project.agents.evaluator import Evaluator
from project.memory.session_memory import SessionMemory
from project.adk.observability import Logger
from project.adk.security_manager import SecurityManager
from project.skills.pii_redactor_skill import PIIRedactorSkill

class MainAgent:
    def __init__(self):
        self.planner = Planner()
        self.worker = Worker()
        self.evaluator = Evaluator()
        self.memory = SessionMemory()
        self.pii_skill = PIIRedactorSkill()

    def handle_message(self, user_input: str) -> dict:
        safe_input = self.pii_skill.execute(text=user_input)
        if safe_input != user_input:
            Logger.log("MainAgent: PII redacted from user input.")

        self.memory.add({"role": "user", "content": safe_input})
        Logger.log("MainAgent initialized workflow.")
        
        plan_msg = self.planner.process(safe_input)
        worker_msg = self.worker.process(plan_msg)
        eval_result = self.evaluator.process(worker_msg)
        
        final_budget = eval_result['final_budget']
        
        SecurityManager.require_hitl_approval(final_budget)
        
        response = f"Final Budget: {final_budget}"
        self.memory.add({"role": "system", "content": response})
        return {"response": response}

def run_agent(user_input: str):
    agent = MainAgent()
    result = agent.handle_message(user_input)
    return result["response"]
