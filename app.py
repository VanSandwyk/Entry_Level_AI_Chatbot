import customtkinter as ctk
from chatbot_engine import ChatbotEngine
import threading

# Set the window theme foundations
ctk.set_appearance_mode("Dark")  # Force Dark Mode as the premium default
ctk.set_default_color_theme("blue")

class ChatbotApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Connect our modular engine
        self.bot_brain = ChatbotEngine(
            system_instruction="You are a helpful, clear, and friendly desktop AI assistant.",
            max_memory=10
        )

        # Window properties
        self.title("Desktop AI Workspace")
        self.geometry("850x650")
        self.minsize(700, 500)

        # Configure Grid Layout (2 Columns: Sidebar + Main Chat)
        self.grid_columnconfigure(0, weight=0) # Sidebar stays fixed width
        self.grid_columnconfigure(1, weight=1) # Chat area scales out dynamically
        self.grid_rowconfigure(0, weight=1)

        # Cache memory for quality-of-life tasks
        self.last_ai_response = ""

        # ==========================================
        # 1. SIDEBAR CONTAINER LAYER
        # ==========================================
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.sidebar.grid_rowconfigure(4, weight=1) # Dynamic empty spacer gap

        # Sidebar Title
        self.logo_label = ctk.CTkLabel(self.sidebar, text="AI Workspace", font=("Segoe UI", 20, "bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))

        # Action Button: Clear Memory
        self.clear_btn = ctk.CTkButton(self.sidebar, text="🗑️  Clear Chat", fg_color="#c0392b", hover_color="#e74c3c", command=self.ui_reset_chat)
        self.clear_btn.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # Action Button: Copy Clipboard Utility
        self.copy_btn = ctk.CTkButton(self.sidebar, text="📋  Copy Last Reply", fg_color="#2c3e50", hover_color="#34495e", command=self.ui_copy_last_reply)
        self.copy_btn.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        # Theme Selector Toggle Box
        self.theme_label = ctk.CTkLabel(self.sidebar, text="Appearance Mode:", font=("Segoe UI", 12))
        self.theme_label.grid(row=5, column=0, padx=20, pady=(10, 2))
        self.theme_menu = ctk.CTkOptionMenu(self.sidebar, values=["Dark", "Light", "System"], command=self.change_appearance_mode)
        self.theme_menu.grid(row=6, column=0, padx=20, pady=(0, 20), sticky="ew")

        # ==========================================
        # 2. MAIN CHAT LAYOUT FRAME
        # ==========================================
        self.chat_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.chat_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.chat_frame.grid_columnconfigure(0, weight=1)
        self.chat_frame.grid_rowconfigure(0, weight=1) # Chat display stretches out vertically

        # Chat Text Display Screen Component
        self.chat_display = ctk.CTkTextbox(self.chat_frame, font=("Segoe UI", 14), state="disabled", wrap="word", border_width=1)
        self.chat_display.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=0, pady=(0, 25))

        # Bottom Entry Panel Configuration
        self.entry_field = ctk.CTkEntry(self.chat_frame, placeholder_text="Ask me anything...", font=("Segoe UI", 14), height=45)
        self.entry_field.grid(row=1, column=0, sticky="ew", padx=(0, 15))
        self.entry_field.bind("<Return>", lambda event: self.send_message())

        self.send_button = ctk.CTkButton(self.chat_frame, text="Send", font=("Segoe UI", 14, "bold"), width=100, height=45, command=self.send_message)
        self.send_button.grid(row=1, column=1, sticky="e")

        # Initial Welcome Message setup
        self.append_to_display("✨ Assistant: Hello Workspace! How can I collaborate with you today?\n\n---------------------------------------------------------------\n\n")

    # ==========================================
    # CORE INTERFACE CONTROLS
    # ==========================================

    def append_to_display(self, text: str):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", text)
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

    def change_appearance_mode(self, new_mode: str):
        ctk.set_appearance_mode(new_mode)

    def ui_reset_chat(self):
        """Maps directly into the engine's clean utility method."""
        self.bot_brain.reset_chat()
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.configure(state="disabled")
        self.append_to_display("✨ System Memory Wiped. Ready for a new topic!\n\n---------------------------------------------------------------\n\n")

    def ui_copy_last_reply(self):
        """Quality of Life utility: Saves the last generated paragraph instantly to clipboard."""
        if self.last_ai_response:
            self.clipboard_clear()
            self.clipboard_append(self.last_ai_response)
            self.copy_btn.configure(text="✅ Copied!")
            self.after(2000, lambda: self.copy_btn.configure(text="📋  Copy Last Reply"))

    def send_message(self):
        user_text = self.entry_field.get().strip()
        if not user_text:
            return

        self.entry_field.delete(0, "end")
        self.append_to_display(f"👤 You: {user_text}\n\n")
        self.append_to_display("✨ Assistant: ")

        # Run connection payload tasks inside background workers to ensure responsive application window layouts
        threading.Thread(target=self.process_ai_response, args=(user_text,), daemon=True).start()

    def process_ai_response(self, user_text: str):
        try:
            stream = self.bot_brain.get_streaming_response(user_text)
            full_answer = ""
            
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    text_chunk = chunk.choices[0].delta.content
                    full_answer += text_chunk
                    self.append_to_display(text_chunk)
                    
            self.append_to_display("\n\n---------------------------------------------------------------\n\n")
            
            # Cache the response string for the clipboard tool utility
            self.last_ai_response = full_answer.strip()
            self.bot_brain.save_bot_response(full_answer)
            
        except Exception as error:
            self.append_to_display(f"\n[ERROR] Could not fetch response: {error}\n\n")

if __name__ == "__main__":
    app = ChatbotApp()
    app.mainloop()
