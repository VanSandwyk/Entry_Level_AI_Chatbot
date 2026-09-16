import os #imports native os packages 
from collections import deque
from dotenv import load_dotenv # loads my API key from .env
from groq import Groq

#Function that loads the .env variable which is my api key 
load_dotenv() 

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key = api_key)
Model_Name = "openai/gpt-oss-20b"

#This is the system Instruction we can change later one that defines the personality of the chatbot
SYSTEM_INSTRUCTION = {"role":"system","content":"You are a helpful, clear, and friendly AI assistant"}

#Now we setup the rolling Window Memory (CAPPED at 10)
rolling_history = deque(maxlen=10)
print("========================================================")
print("Statefull chatbot Ready")
print("type 'quit' or 'exit' to turn off engine")
print("========================================================")

while True:
    user_input = input("\n Type your message: ")

    if user_input.lower() in ["quit","exit"]: #checks for stop case
        print("Goodbye")
        break
    if not user_input.strip():
        continue

    rolling_history.append({"role":"user","content":user_input})
    payload = [SYSTEM_INSTRUCTION]+ list(rolling_history)

    print("AI is thinking")

    try:
        response = client.chat.completions.create(
            model=Model_Name,
            messages=payload
        )

        ai_answer = response.choices[0].message.content
        print(f"\nAssistant: {ai_answer}")

        rolling_history.append({"role":"assistant","content":ai_answer})

    except Exception as e:
        print(f"\n An error occured: {e}")