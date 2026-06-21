class AgentSkill:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def execute(self, **kwargs):
        raise NotImplementedError("Skills must implement execute()")
