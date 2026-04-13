import socket
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox

HOST = "127.0.0.1"
PORT = 8888

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((HOST, PORT))
except:
    messagebox.showerror("Error", "Cannot connect to server.\nMake sure server_gui.py is running first.")
    raise SystemExit

root = tk.Tk()
root.title("Chat Application")
root.geometry("500x500")
root.resizable(False, False)

chat_box = tk.Text(root, state="disabled", wrap="word", font=("Arial", 11))
chat_box.pack(padx=10, pady=10, fill="both", expand=True)

bottom_frame = tk.Frame(root)
bottom_frame.pack(fill="x", padx=10, pady=10)

message_entry = tk.Entry(bottom_frame, font=("Arial", 11))
message_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

def add_message(message):
    chat_box.config(state="normal")
    chat_box.insert(tk.END, message + "\n")
    chat_box.config(state="disabled")
    chat_box.see(tk.END)

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == "NAME":
                client.send(username.encode())
            else:
                root.after(0, add_message, message)
        except:
            break

def send_message():
    text = message_entry.get().strip()
    if text:
        full_message = f"{username}: {text}"
        try:
            client.send(full_message.encode())
            add_message(full_message)
            message_entry.delete(0, tk.END)
        except:
            messagebox.showerror("Error", "Message failed to send.")

def on_enter(event):
    send_message()

def on_close():
    try:
        client.close()
    except:
        pass
    root.destroy()

username = simpledialog.askstring("Name", "Enter your name:")
if not username:
    username = "User"

send_button = tk.Button(bottom_frame, text="Send", width=10, command=send_message)
send_button.pack(side="right")

message_entry.bind("<Return>", on_enter)

thread = threading.Thread(target=receive_messages, daemon=True)
thread.start()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()