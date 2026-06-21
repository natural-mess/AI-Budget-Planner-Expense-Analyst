class SessionMemory:
    def __init__(self):
        self.history = []
        
    def add(self, item: dict):
        self.history.append(item)
        
    def get_all(self):
        return self.history
