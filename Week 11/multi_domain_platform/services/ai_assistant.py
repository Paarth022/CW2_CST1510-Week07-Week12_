from typing import List, Dict

class AIAssistant:
    
    
    def __init__(self, system_prompt: str = "You are a helpful assistant."):
        
        self._system_prompt = system_prompt
        self._history: List[Dict[str, str]] = []
    
    def set_system_prompt(self, prompt: str) -> None:
        
        self._system_prompt = prompt
    
    def get_system_prompt(self) -> str:
       
        return self._system_prompt
    
    def send_message(self, user_message: str) -> str:
        # Add user message to history
        self._history.append({
            "role": "user",
            "content": user_message
        })
        
        # Mock response (replace with real API call)
        response = f"[AI Assistant] Processing: {user_message[:50]}..."
        
        # Add assistant response to history
        self._history.append({
            "role": "assistant",
            "content": response
        })
        
        return response
    
    def get_history(self) -> List[Dict[str, str]]:
        return self._history
    
    def clear_history(self) -> None:
        self._history.clear()
    
    def __str__(self) -> str:
        return f"AIAssistant(prompt='{self._system_prompt}', messages={len(self._history)})"