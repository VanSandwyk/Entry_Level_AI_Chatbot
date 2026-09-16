import sys
from chatbot_engine import ChatbotEngine

# Initialize our decoupled modular engine
bot_brain = ChatbotEngine(
    system_instruction="You are a helpful, clear, and friendly AI assistant.",
    max_memory=10
)

print("==========================================================")
print("Modular Production Engine Active (Class-Based Architecture)")
print("Type 'quit' or 'exit' to turn off the engine.")
print("==========================================================")

while True:
    try:
        user_input = input("\nYou: ")
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
        break
        
    if user_input.lower() in ["quit", "exit"]:
        print("Goodbye!")
        break
        
    if not user_input.strip():
        continue
        
    print("\nAssistant: ", end="", flush=True)
    
    try:
        # Get the stream stream from our modular class
        stream = bot_brain.get_streaming_response(user_input)
        
        full_answer = ""
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                text_chunk = chunk.choices[0].delta.content
                print(text_chunk, end="", flush=True)
                full_answer += text_chunk
        print()
        
        # Tell the engine to commit the final string to memory
        bot_brain.save_bot_response(full_answer)
        
    except Exception as network_error:
        print(f"\n[NETWORK ERROR] Could not get response: {network_error}")