import re
from adk.skill_base import AgentSkill

class PIIRedactorSkill(AgentSkill):
    def __init__(self):
        super().__init__(name="pii_redactor", description="Redacts PII like SSNs from text.")

    def execute(self, text: str):
        return re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[REDACTED SSN]', text)
