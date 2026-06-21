class Tools:
    @staticmethod
    def calculator(expression: str):
        try:
            return eval(expression)
        except Exception as e:
            return str(e)
            
    @staticmethod
    def summarize(text: str):
        return text[:100] + "..." if len(text) > 100 else text
