#  Custom AI Desktop Companion

A production-grade, secure desktop chatbot built natively in **Python**. This project demonstrates modular architecture by decoupling a robust, stateful AI engine from a modern, multi-threaded user interface shell. 



* **Decoupled Architecture (OOP)**: Core AI orchestration logic is entirely isolated into a reusable `ChatbotEngine` class, making it completely independent of the UI layer.
* **Stateful Rolling Memory**: Utilizes a customized double-ended queue (`deque`) capped at 10 items. This preserves context and prevents memory bloating, token overhead, or context window crashes, while permanently retaining global system instructions.
* **Multi-Threaded UI Interface**: Leverages background thread offloading (`threading.Thread`) to process network operations asynchronously. This keeps the user interface responsive and fluid while text streams over the web.
* **Asynchronous Markdown Parser**: Features a regex-driven typography parser that catches raw markdown chunks and translates them on-the-fly into styled header weights and bold accent typography layout tags.
* **Quality of Life Utilities**: Integrated native operating system clipboard integration for instant reply copying, an engine-mapped session reset function, and custom theme runtime switching (Dark/Light).



* **Language**: Python 3.x
* **AI Provider**: Groq API (Inference Engine)
* **Model Layout**: `openai/gpt-oss-20b` (API Interoperability Standard)
* **GUI Engine**: CustomTkinter (Modernized rendering framework)
* **Environment Security**: Python-Dotenv



```text
├── .env                # HIDE FROM GIT: Secret cloud API entry credentials
├── .gitignore          # Rules defining excluded cache and environment modules
├── app.py              # Main desktop window thread event listener and UI layout
├── bot.py              # Lightweight fallback terminal execution harness 
├── chatbot_engine.py   # Isolated Object-Oriented AI brain & memory pipeline
└── README.md           # Professional project documentation
```



### 1. Prerequisites
Ensure Python 3.x is configured globally on your machine. Check this via your command prompt:
```bash
python --version
```

### 2. Clone the Workspace & Install Dependencies
```bash
git clone <YOUR_REPOSITORY_URL_HERE>
cd <YOUR_PROJECT_FOLDER_NAME>
pip install groq python-dotenv customtkinter
```

### 3. Secure Your Credentials
Create a hidden environment file named `.env` in the root folder directory and inject your verified API key exactly as follows:
```text
GROQ_API_KEY=your_actual_api_key_here
```

### 4. Run the Engine
To boot the desktop environment application workspace interface:
```bash
python app.py
```
