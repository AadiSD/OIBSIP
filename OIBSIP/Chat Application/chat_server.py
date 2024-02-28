import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

class ChatServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Server")

        # Create and configure the GUI components
        self.message_list = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
        self.message_list.grid(row=0, column=0, padx=10, pady=10)

        self.entry_message_server = tk.Entry(root, width=40)
        self.entry_message_server.grid(row=1, column=0, padx=10, pady=10)

        self.send_button_server = tk.Button(root, text="Send to Clients", command=self.send_message_server)
        self.send_button_server.grid(row=1, column=1, padx=10, pady=10)

        # Create a socket for the server
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 5556))
        self.server_socket.listen(5)
        self.message_list.insert(tk.END, "Server listening for connections...\n")

        # List to store client sockets
        self.clients = []

        # Start accepting connections in a separate thread
        accept_thread = threading.Thread(target=self.accept_connections)
        accept_thread.start()

    def broadcast_message(self, message, sender_socket):
        for client_socket in self.clients:
            if client_socket != sender_socket:
                try:
                    client_socket.send(message.encode("utf-8"))
                except:
                    self.remove_client(client_socket)

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode("utf-8")
                if not message:
                    self.remove_client(client_socket)
                    break
                self.message_list.insert(tk.END, f"Client: {message}\n")
                self.broadcast_message(f"Client: {message}", client_socket)
            except:
                self.remove_client(client_socket)
                break

    def remove_client(self, client_socket):
        if client_socket in self.clients:
            self.clients.remove(client_socket)
            client_socket.close()

    def accept_connections(self):
        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                self.clients.append(client_socket)
                self.message_list.insert(tk.END, f"Connection established with {client_address}\n")
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()
            except Exception as e:
                print(f"An error occurred while accepting connections: {e}")

    def send_message_server(self):
        message = self.entry_message_server.get()
        if message:
            try:
                for client_socket in self.clients:
                    client_socket.send(f"Server: {message}".encode("utf-8"))
                self.message_list.insert(tk.END, f"Server: {message}\n")
                self.entry_message_server.delete(0, tk.END)
            except:
                print("Failed to send message to clients.")

    def run(self):
        self.root.mainloop()
        # Close server socket when GUI is closed
        self.server_socket.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatServerApp(root)
    app.run()
