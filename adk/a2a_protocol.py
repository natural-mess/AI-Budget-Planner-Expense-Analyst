import json

class Message:
    def __init__(self, sender: str, receiver: str, task: str, data: dict):
        self.sender = sender
        self.receiver = receiver
        self.task = task
        self.data = data
        
    def to_json(self):
        return json.dumps(self.__dict__)
