import customtkinter as ctk
from chatbot_engine import ChatbotEngine
import threading
import re

ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("blue")

class ChatbotApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.bot_brain = ChatbotEngine(
            system_instruction="You are a helpful, clear, and friendly desktop AI assistant.",
            max_memory=10
        )

        self.title("AI Workspace Pro")
        self.geometry("900x700")
        self.minsize(750, 550)

        self.grid_columnconfigure(0, weight=0) 
        self.grid_columnconfigure(1, weight=1) 
        self.grid_rowconfigure(0, weight=1)

        self.last_ai_response = ""

   
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#1a1a1a")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1) 

        self.logo_label = ctk.CTkLabel(self.sidebar, text="🤖 Workspace Pro", font=("Segoe UI", 20, "bold"), text_color="#3b82f6")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 40))

        self.clear_btn = ctk.CTkButton(self.sidebar, text="🗑️  Clear Workspace", font=("Segoe UI", 13, "bold"), fg_color="#ef4444", hover_color="#dc2626", height=40, command=self.ui_reset_chat)
        self.clear_btn.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.copy_btn = ctk.CTkButton(self.sidebar, text="📋  Copy Response", font=("Segoe UI", 13, "bold"), fg_color="#2b2d42", hover_color="#3d405b", height=40, command=self.ui_copy_last_reply)
        self.copy_btn.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.theme_label = ctk.CTkLabel(self.sidebar, text="Appearance:", font=("Segoe UI", 12), text_color="#888888")
        self.theme_label.grid(row=5, column=0, padx=20, pady=(10, 2))
        self.theme_menu = ctk.CTkOptionMenu(self.sidebar, values=["Dark", "Light", "System"], command=ctk.set_appearance_mode)
        self.theme_menu.grid(row=6, column=0, padx=20, pady=(0, 25), sticky="ew")

   
        self.chat_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.chat_frame.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)
        self.chat_frame.grid_columnconfigure(0, weight=1)
        self.chat_frame.grid_rowconfigure(0, weight=1) 

        # Text Screen Display Area
        self.chat_display = ctk.CTkTextbox(
            self.chat_frame, 
            font=("Segoe UI", 14), 
            state="disabled", 
            wrap="word", 
            border_width=1,
            fg_color="#1e1e2e",
            text_color="#cdd6f4",
            border_color="#313244"
        )
        self.chat_display.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=0, pady=(0, 25))

     
        # These rules intercept text styles and format them beautifully on the fly
        self.chat_display._textbox.tag_config("user_header", font=("Segoe UI", 14, "bold"), foreground="#a6e3a1")
        self.chat_display._textbox.tag_config("bot_header", font=("Segoe UI", 14, "bold"), foreground="#89b4fa")
        self.chat_display._textbox.tag_config("bold", font=("Segoe UI", 14, "bold"), foreground="#f38ba8")
        self.chat_display._textbox.tag_config("markdown_h3", font=("Segoe UI", 18, "bold"), foreground="#89dceb")
        self.chat_display._textbox.tag_config("divider", font=("Segoe UI", 12), foreground="#45475a")

        # Input Control Panel
        self.entry_field = ctk.CTkEntry(self.chat_frame, placeholder_text="Ask a question or request a layout...", font=("Segoe UI", 14), height=48, fg_color="#181825", border_color="#313244")
        self.entry_field.grid(row=1, column=0, sticky="ew", padx=(0, 15))
        self.entry_field.bind("<Return>", lambda event: self.send_message())

        self.send_button = ctk.CTkButton(self.chat_frame, text="Send", font=("Segoe UI", 14, "bold"), width=110, height=48, fg_color="#3b82f6", hover_color="#2563eb", command=self.send_message)
        self.send_button.grid(row=1, column=1, sticky="e")

        self.inject_styled_block("✨ Workspace Active. How can I assist you today?\n\n", "bot_header")
        self.inject_styled_block("---------------------------------------------------------------\n\n", "divider")



    def inject_styled_block(self, text: str, tag: str = None):
        """Safely inserts a block of text bound to a specific typographical style tag."""
        self.chat_display.configure(state="normal")
        if tag:
            self.chat_display.insert("end", text, tag)
        else:
            self.chat_display.insert("end", text)
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

    def render_clean_markdown(self, raw_text: str):
        """
        Parses raw text, strips out messy markdown tokens (*, #), 
        and prints beautifully formatted rich text directly to the UI panel.
        """
        lines = raw_text.split('\n')
        for line in lines:
            # 1. Parse Subheadings (e.g., ### Section)
            if line.strip().startswith("###"):
                clean_line = line.replace("###", "").strip()
                self.inject_styled_block(f"\n{clean_line}\n", "markdown_h3")
                continue
            
            # 2. Parse Section Dividers
            if line.strip() == "---":
                self.inject_styled_block("_______________________________________________________________\n\n", "divider")
                continue

            # 3. Parse Inline Bold elements (e.g., **text**)
            # This regex looks for text wrapped in double asterisks
            parts = re.split(r'(\*\*.*?\*\*)', line)
            for part in parts:
                if part.startswith("**") and part.endswith("**"):
                    clean_bold = part.replace("**", "")
                    self.inject_styled_block(clean_bold, "bold")
                else:
                    self.inject_styled_block(part)
            
            # Add line break at the end of each line item row
            self.inject_styled_block("\n")



    def ui_reset_chat(self):
        self.bot_brain.reset_chat()
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.configure(state="disabled")
        self.inject_styled_block("✨ System Memory Reset.\n\n", "bot_header")
        self.inject_styled_block("---------------------------------------------------------------\n\n", "divider")

    def ui_copy_last_reply(self):
        if self.last_ai_response:
            self.clipboard_clear()
            self.clipboard_append(self.last_ai_response)
            self.copy_btn.configure(text="✅ Copied!")
            self.after(2000, lambda: self.copy_btn.configure(text="📋  Copy Response"))

    def send_message(self):
        user_text = self.entry_field.get().strip()
        if not user_text:
            return

        self.entry_field.delete(0, "end")
        self.inject_styled_block("👤 You: ", "user_header")
        self.inject_styled_block(f"{user_text}\n\n")
        self.inject_styled_block("✨ Assistant:\n", "bot_header")

        threading.Thread(target=self.process_ai_response, args=(user_text,), daemon=True).start()

    def process_ai_response(self, user_text: str):
        try:
            stream = self.bot_brain.get_streaming_response(user_text)
            full_answer = ""
            
            # To ensure layout structural integrity, we capture the streaming text response block 
            # and render it via the layout manager immediately as it finishes compiling.
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    full_answer += chunk.choices[0].delta.content
            
            # Render the final clean, parsed text block
            self.render_clean_markdown(full_answer)
            self.inject_styled_block("_______________________________________________________________\n\n", "divider")
            
            self.last_ai_response = full_answer.strip()
            self.bot_brain.save_bot_response(full_answer)
            
        except Exception as error:
            self.inject_styled_block(f"\n[ERROR] Could not fetch response: {error}\n\n", "bold")

if __name__ == "__main__":
    app = ChatbotApp()
    app.mainloop()
