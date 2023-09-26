import tkinter as tk
from tkinter import Scrollbar, Text
import openai
#import config

openai.api_key = "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"

class ChatApp:
    
    def send_on_enter(self, event):
        self.send_message()
     
    def __init__(self, root):
        self.root = root
        self.root.title("Chat con Asistente")
        
        self.root.configure(bg="#121212")
        
        
        self.chat_box = Text(root, wrap="word", state="disabled", bg="#121212", fg="white")  # Cambiar el color de fondo y letras
        self.scrollbar = Scrollbar(root, command=self.chat_box.yview, bg="#121212")
        self.chat_box.config(yscrollcommand=self.scrollbar.set)
        
        self.user_input = tk.Entry(root, bg="#121212", fg="white")  # Cambiar el color de fondo y letras
        self.send_button = tk.Button(root, text="Enviar", command=self.send_message, bg="#333", fg="white")  # Cambiar los colores de fondo y letras
        
        self.chat_box.pack(side="top", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.user_input.pack(side="left", fill="x", expand=True)
        self.send_button.pack(side="right")
        
        self.messages = [{"role": "system", "content": "¡Hola! Soy tu asistente virtual."}]
        self.update_chat_display()
        
        self.user_input.bind("<Return>", self.send_on_enter)
        
    def send_message(self):
        user_content = self.user_input.get()
        self.user_input.delete(0, "end")
        
        if user_content.lower() in ["exit", "cerrar"]:
            self.root.destroy()
            return
        
        self.messages.append({"role": "user", "content": user_content})
        response = self.get_assistant_response(user_content)
        self.messages.append({"role": "assistant", "content": response})
        
        self.update_chat_display()
    
    def get_assistant_response(self, user_input):
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages)
        return response.choices[0].message['content']
    
    def update_chat_display(self):
        self.chat_box.config(state="normal")
        self.chat_box.delete(1.0, "end")
        
        for message in self.messages:
            role = message["role"]
            content = message["content"]
            self.chat_box.insert("end", f"{role.capitalize()}: {content}\n\n")
        
        self.chat_box.config(state="disabled")
        self.chat_box.see("end")
    
    def run_console_interaction(self):
        while True:
            content = input("Sobre qué quieres hablar? ")

            if content == "exit" or content == "cerrar":
                self.root.destroy()
                return

            self.messages.append({"role": "user", "content": content})
            response = self.get_assistant_response(content)
            self.messages.append({"role": "assistant", "content": response})

            self.update_chat_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    
    if __name__ == "__main__":
        root = tk.Tk()
        app = ChatApp(root)
        
        if len(app.messages) == 1 and app.messages[0]["content"] == "¡Hola! Soy tu asistente virtual.":
            app.run_console_interaction()
        else:
            root.mainloop()



        
      