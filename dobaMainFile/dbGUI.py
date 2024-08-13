import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from dbSSHCred import SSHCredentialsManager
import logging
import os
import json

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class App:
    def __init__(self, root, upload_logic):
        self.root = root
        self.upload_logic = upload_logic
        self.credentials_manager = SSHCredentialsManager()
        self.ssh_credentials = self.credentials_manager.load_credentials()
        self.root.title("DocuBase Folder Watchdog")
        self.root.geometry("350x150")
        self.root.resizable(False, False)  # Disable resizing
        
        self.directory_to_watch = tk.StringVar()
        self.load_directory_from_file()  # Load the directory path
        self.create_widgets()
        self.print_credentials_directory()

    def create_widgets(self):
        # Create the menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        self.options_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Options", menu=self.options_menu)
        self.options_menu.add_command(label="Set SSH Credentials", command=self.open_ssh_credentials_dialog)
        self.options_menu.add_command(label="Check SSH Credentials", command=self.check_ssh_credentials)
 
        
        ttk.Label(self.root, text="Directory to Watch: ").pack(pady=5)
        self.directory_entry = ttk.Entry(self.root, textvariable=self.directory_to_watch, width=40)
        self.directory_entry.pack(pady=5)
        
        self.select_folder_btn = ttk.Button(self.root, text="Select Folder", command=self.browse_directory, width=20)
        self.select_folder_btn.pack(pady=5)
        
        self.start_button = ttk.Button(self.root, text="Start Watchdog", command=self.start_watching, width=20)
        self.start_button.pack(pady=5)
        
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory_to_watch.set(directory)
            self.save_directory_to_file(directory)  # Save the directory path
    
    def start_watching(self):
        directory = self.directory_to_watch.get()
        if os.path.isdir(directory):
            self.upload_logic.start_watcher(directory)
            self.start_button.config(state=tk.DISABLED)
            messagebox.showinfo("Information", "Started watching the directory")
        else:
            messagebox.showerror("Error", "Invalid Directory")

        
    def open_ssh_credentials_dialog(self):
        # Create a new top-level window for SSH credentials input
        dialog = tk.Toplevel(self.root)
        dialog.title("SSH Credentials")
        dialog.geometry("300x200")
        dialog.resizable(False, False)  # Disable resizing for the dialog
        
        tk.Label(dialog, text="Server IP:").grid(row=0, column=0, padx=10, pady=5)
        self.host_entry = tk.Entry(dialog)
        self.host_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Port:").grid(row=1, column=0, padx=10, pady=5)
        self.port_entry = tk.Entry(dialog)
        self.port_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Server Username:").grid(row=2, column=0, padx=10, pady=5)
        self.username_entry = tk.Entry(dialog)
        self.username_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Server Password:").grid(row=3, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(dialog)
        self.password_entry.grid(row=3, column=1, padx=10, pady=5)
        
        tk.Label(dialog,text="Folder Destination").grid(row=4,column=0, padx=10, pady=5)
        self.fdest_entry = tk.Entry(dialog)
        self.fdest_entry.grid(row=4, column=1, padx=10, pady=5)
        
        tk.Button(dialog, text="Save", command=self.save_ssh_credentials).grid(row=5, column=0, columnspan=2, pady=10)
    
    def save_ssh_credentials(self):
        self.ssh_credentials = {
            "host": self.host_entry.get(),
            "port": self.port_entry.get(),
            "username": self.username_entry.get(),
            "password": self.password_entry.get(),
            "folderdestination": self.fdest_entry.get()
        }
        self.credentials_manager.save_credentials(self.ssh_credentials)
        messagebox.showinfo("Information", "SSH Credentials have been saved.")
        self.host_entry.master.destroy()
    
    def check_ssh_credentials(self):
        # Load the credentials from the manager
        creds = self.credentials_manager.load_credentials()
        
        if not creds:
            messagebox.showinfo("SSH Credentials", "No credentials have been saved.")
        else:
            # Create a formatted string to display the credentials
            credentials_info = (
                f"Host: {creds['host']}\n"
                f"Port: {creds['port']}\n"
                f"Username: {creds['username']}\n"
                f"Password: {creds['password']}\n"
                f"Folder Destination: {creds['folderdestination']}\n"
            )
            print("CHECK SSH CREDS" + credentials_info)
            messagebox.showinfo("SSH Credentials", credentials_info)
            
             
    def save_directory_to_file(self, directory):
        data = {"directory": directory}
        with open("config.json", "w") as file:
            json.dump(data, file)

    def load_directory_from_file(self):
        if os.path.exists("config.json"):
            with open("config.json", "r") as file:
                data = json.load(file)
                directory = data.get("directory", "")
                self.directory_to_watch.set(directory)

    def print_credentials_directory(self):
        directory = self.credentials_manager.get_credentials_path()
        logging.debug(f"SSH Credentials are saved in: {directory}")
        print(f"SSH Credentials are saved in: {directory}")
