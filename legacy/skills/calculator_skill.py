from adk.skill_base import AgentSkill

class CalculatorSkill(AgentSkill):
    def __init__(self):
        super().__init__(name="calculator", description="Performs basic arithmetic.")

    def execute(self, expression: str):
        try:
            return eval(expression)
        except Exception as e:
            return str(e)
