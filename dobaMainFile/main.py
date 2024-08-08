import tkinter as tk
from dbGUI import App
from dbMonitor import UploadLogic
import json
import os

def load_ssh_credentials():
    path = os.path.join(os.getenv('APPDATA', os.path.expanduser('~')), "ssh_credentials.json")
    if os.path.exists(path):
        with open(path, "r") as file:
            return json.load(file)
    return {"host": "", "port": "", "username": "", "password": ""}

if __name__ == "__main__":
    ssh_credentials = load_ssh_credentials()
    upload_logic = UploadLogic(ssh_credentials)
    
    root = tk.Tk()
    app = App(root, upload_logic)
    root.mainloop()