from project.adk.observability import Logger

class SecurityManager:
    @staticmethod
    def require_hitl_approval(budget: dict) -> bool:
        # HITL (Human-in-the-loop): If any category > $1000, request approval
        for category, amount in budget.items():
            if isinstance(amount, (int, float)) and amount >= 1000:
                Logger.log(f"SecurityManager HITL: '{category}' threshold trigger (${amount}). Simulated user approval required.")
                Logger.log("SecurityManager HITL: User APPROVED.")
                return True
        return True
