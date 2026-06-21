from adk.observability import Logger
from adk.llm_client import LLMClient

class BaseAgent:
    def __init__(self, name: str, context: str):
        self.name = name
        self.context = context
        self.skills = []
        self.llm = LLMClient()

    def equip_skill(self, skill):
        self.skills.append(skill)
        Logger.log(f"{self.name} equipped skill: {skill.name}")

    def execute_skill(self, skill_name: str, **kwargs):
        for skill in self.skills:
            if skill.name == skill_name:
                return skill.execute(**kwargs)
        raise ValueError(f"Skill {skill_name} not found on {self.name}")

    def process(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement process()")
