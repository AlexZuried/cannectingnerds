import requests
import json

class OllamaClient:
    def __init__(self, host="http://localhost:11434", model="llama3.2"):
        self.host = host
        self.model = model
    
    def generate(self, prompt, context=""):
        """Generate response using local Ollama model"""
        full_prompt = f"{context}\n\n{prompt}" if context else prompt
        
        try:
            response = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": full_prompt,
                    "stream": False
                },
                timeout=60
            )
            return response.json().get("response", "")
        except Exception as e:
            print(f"Ollama error: {e}")
            return ""
    
    def is_available(self):
        """Check if Ollama is running"""
        try:
            r = requests.get(f"{self.host}/api/tags", timeout=5)
            return r.status_code == 200
        except:
            return False
