import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

class ChatClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client")

        # Create and configure the GUI components
        self.message_list = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
        self.message_list.grid(row=0, column=0, padx=10, pady=10)

        self.entry_message = tk.Entry(root, width=40)
        self.entry_message.grid(row=1, column=0, padx=10, pady=10)

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        # Create a socket for the client
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 5556))

        # Start receiving messages in a separate thread
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

    def send_message(self):
        message = self.entry_message.get()
        if message:
            try:
                self.client_socket.send(message.encode("utf-8"))
                self.entry_message.delete(0, tk.END)
            except:
                print("Failed to send message. Connection may be closed.")

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode("utf-8")
                self.message_list.insert(tk.END, message + "\n")
                self.message_list.yview(tk.END)
            except:
                print("Failed to receive message. Connection may be closed.")
                break

    def run(self):
        self.root.mainloop()
        # Close client socket when GUI is closed
        self.client_socket.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClientApp(root)
    app.run()
