import tkinter as tk
from tkinter import Scrollbar, Text
import openai
import config
import threading
import time

openai.api_key = config.api

class ChatApp:
    def send_on_enter(self, event):
        self.send_message()
     
    def __init__(self, root):
        self.root = root
        self.root.title("Chat con Asistente")
        
        self.root.configure(bg="#121212")
        
        self.chat_box = Text(root, wrap="word", state="disabled", bg="#121212", fg="white")
        self.scrollbar = Scrollbar(root, command=self.chat_box.yview, bg="#121212")
        self.chat_box.config(yscrollcommand=self.scrollbar.set)
        
        self.user_input = tk.Entry(root, bg="#121212", fg="white")
        self.send_button = tk.Button(root, text="Enviar", command=self.send_message, bg="#333", fg="white")
        
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
        self.update_chat_display()
        
        # Mostrar el mensaje "Escribiendo..."
        writing_message = {"role": "assistant", "content": "Escribiendo..."}
        self.messages.append(writing_message)
        self.update_chat_display()
        
        # Crear un nuevo hilo para obtener y mostrar la respuesta del asistente
        thread = threading.Thread(target=self.get_and_display_assistant_response, args=(user_content,))
        thread.start()
        
        # Agregar los puntos suspensivos progresivamente y repetir hasta recibir la respuesta
        while writing_message in self.messages:
            for i in range(3):
                time.sleep(0.2)
                if writing_message in self.messages:
                    self.messages[-1]["content"] = "Escribiendo" + "." * (i + 1)
                    self.update_chat_display()

    def get_and_display_assistant_response(self, user_input):
        response = self.get_assistant_response(user_input)
        self.messages[-1] = {"role": "assistant", "content": "Escribiendo"}
        self.update_chat_display()
        
        response_content = ""
        for char in response:
            response_content += char
            self.messages[-1]["content"] = response_content
            self.update_chat_display()
            time.sleep(0.05)
        
        self.messages[-1]["content"] = response
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

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()