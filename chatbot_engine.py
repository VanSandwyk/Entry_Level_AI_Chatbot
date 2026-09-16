import os
import sys
from collections import deque
from dotenv import load_dotenv
from groq import Groq

class ChatbotEngine:
    def __init__(self, system_instruction: str = "You are a helpful AI assistant.", max_memory: int = 10):
        """Initializes the secure AI engine and memory structures."""
        load_dotenv()
        self.api_key = os.getenv("GROQ_API_KEY")
        
        # Security Guardrail
        if not self.api_key:
            print("\n[SECURITY ERROR] Missing GROQ_API_KEY in environment variables!")
            sys.exit(1)
            
        self.client = Groq(api_key=self.api_key)
        self.model_name = "openai/gpt-oss-20b"
        
        # Core Rules and Memory
        self.system_instruction = {"role": "system", "content": system_instruction}
        self.rolling_history = deque(maxlen=max_memory)

    def get_streaming_response(self, user_message: str):
        """
        Sends the user message along with memory context to the API.
        Returns a generator object for real-time word streaming.
        """
        # Save user message to memory
        self.rolling_history.append({"role": "user", "content": user_message})
        
        # Combine fixed instruction with shifting memory
        payload = [self.system_instruction] + list(self.rolling_history)
        
        try:
            # Secure network call with streaming enabled
            response_stream = self.client.chat.completions.create(
                model=self.model_name,
                messages=payload,
                temperature=0.7,
                stream=True 
            )
            return response_stream
            
        except Exception as e:
            # If the network or API fails, clean up the last message so memory doesn't desync
            if self.rolling_history:
                self.rolling_history.pop()
            raise RuntimeError(f"API Connection Failure: {e}")

    def save_bot_response(self, full_ai_answer: str):
        """Saves the completed AI response back into memory once streaming finishes."""
        self.rolling_history.append({"role": "assistant", "content": full_ai_answer})

#=========================================================
#UI Implementations Methods
#=========================================================
def get_chat_history(self):
    """
    Returns a clean list of the current active dialogue logs.
    Also excludes the hidden system instructions so that the UI only renders the actual user vs assistant convo
    """

    return list(self.rolling_history)

def reset_chat(self):
    """
    a method that clears out all data logs from memory 
    """