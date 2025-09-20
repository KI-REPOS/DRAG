from llama_cpp import Llama
from typing import List, Dict, Any
import re
from config import Config

class LocalLLM:
    def __init__(self):
        self.model = Llama(
            model_path=Config.LLM_MODEL_PATH,
            n_ctx=Config.MAX_CONTEXT_LENGTH,
            n_threads=4,
            n_gpu_layers=0,  # Set to >0 if you have GPU
            verbose=False
        )
    
    def generate_response(self, prompt: str, max_tokens: int = 512) -> str:
        """Generate response using local LLM."""
        try:
            output = self.model(
                prompt,
                max_tokens=max_tokens,
                temperature=0.1,
                top_p=0.9,
                echo=False,
                stop=["###", "Human:", "Assistant:"]
            )
            
            response = output['choices'][0]['text'].strip()
            return self._clean_response(response)
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I apologize, but I encountered an error while generating a response."
    
    def _clean_response(self, response: str) -> str:
        """Clean and format the response."""
        # Remove any incomplete sentences at the end
        response = re.sub(r'[^.!?]+$', '', response)
        # Ensure proper capitalization
        if response and response[0].islower():
            response = response[0].upper() + response[1:]
        return response.strip()
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text (approximate)."""
        return len(text.split())  # Simple approximation
    
    def truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        """Truncate text to maximum number of tokens."""
        words = text.split()
        if len(words) <= max_tokens:
            return text
        return ' '.join(words[:max_tokens])

class ConversationManager:
    def __init__(self, llm: LocalLLM):
        self.llm = llm
        self.conversation_history: List[Dict[str, str]] = []
        self.max_history_tokens = 1000
    
    def add_message(self, role: str, content: str):
        """Add message to conversation history."""
        self.conversation_history.append({"role": role, "content": content})
        self._manage_history_size()
    
    def get_conversation_context(self) -> str:
        """Get formatted conversation context."""
        context = ""
        for msg in self.conversation_history:
            context += f"{msg['role'].capitalize()}: {msg['content']}\n\n"
        return context.strip()
    
    def _manage_history_size(self):
        """Manage conversation history size to avoid exceeding token limits."""
        total_tokens = sum(self.llm.count_tokens(msg["content"]) 
                          for msg in self.conversation_history)
        
        while total_tokens > self.max_history_tokens and len(self.conversation_history) > 1:
            # Remove oldest non-system message
            removed = None
            for i, msg in enumerate(self.conversation_history):
                if msg["role"] != "system":
                    removed = self.conversation_history.pop(i)
                    break
            
            if removed:
                total_tokens -= self.llm.count_tokens(removed["content"])
            else:
                break
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []