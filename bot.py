import os #imports native os packages 
import sys
from collections import deque
from dotenv import load_dotenv # loads my API key from .env
from groq import Groq

#Function that loads the .env variable which is my api key 
load_dotenv() 

api_key = os.getenv("GROQ_API_KEY")
if not api_key or api_key == "your_actual_api_key_here":
    print("\n [SECURITY ERROR] Missing API Key!")
    print("Please ensure '.env' file exists and contains : GROQ_API_KEY=your_key")
    sys.exit(1)


#Initialization
client = Groq(api_key = api_key)
Model_Name = "openai/gpt-oss-20b"

#============================================
# Chatbot Core
#============================================

#This is the system Instruction we can change later one that defines the personality of the chatbot
SYSTEM_INSTRUCTION = {"role":"system","content":"You are a helpful, clear, and friendly AI assistant"}
#Now we setup the rolling Window Memory (CAPPED at 10)
rolling_history = deque(maxlen=10)

print("========================================================")
print("Production Engine Active")
print("type 'quit' or 'exit' to turn off engine")
print("========================================================")

#=============================================
# Interaction loop
#=============================================

while True:
    try:
        user_input = input("\n Type your message: ")
    except (KeyboardInterrupt,EOFError):
        print("\n Goodbye")
        break

    if user_input.lower() in ["quit","exit"]: #checks for stop case
        print("Goodbye")
        break
    if not user_input.strip():
        continue

    rolling_history.append({"role":"user","content":user_input})
    payload = [SYSTEM_INSTRUCTION]+ list(rolling_history)

    print("\nAssistant: ",end="",flush=True)

    try:
        response_stream = client.chat.completions.create(
            model=Model_Name,
            messages=payload,
            temperature=0.7,  #Balance between consistency and natuaral flow
            stream=True       #Allows text delivery token by token
        )

        full_ai_answer = ""

        for chunk in response_stream:
            if chunk.choices and chunk.choices[0].delta.content:
                text_chunk = chunk.choices[0].delta.content
                print(text_chunk,end="",flush=True) #prints instant word by word
                full_ai_answer += text_chunk

        print()

        rolling_history.append({"role": "assistant", "content": full_ai_answer})
                

    except Exception as e:
        print(f"\n An error occured: {e}")