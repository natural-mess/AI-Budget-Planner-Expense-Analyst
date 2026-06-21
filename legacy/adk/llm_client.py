import google.generativeai as genai
from adk.observability import Logger

class LLMClient:
    def generate(self, prompt: str, api_key: str = None, require_json: bool = False) -> str:
        if not api_key:
            Logger.log("LLMClient: No API key provided, returning mocked response.")
            return '{"Housing": 1200, "Food": 400, "Savings": 500, "strategy": "Mocked due to missing API key"}' if require_json else "Missing API Key."
        
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-pro")
            generation_config = {"response_mime_type": "application/json"} if require_json else None
            
            response = model.generate_content(prompt, generation_config=generation_config)
            return response.text
        except Exception as e:
            Logger.log(f"LLMClient Generation Error: {e}")
            return '{"Housing": 1200, "Food": 400, "Savings": 500, "strategy": "Fallback due to error"}' if require_json else str(e)
