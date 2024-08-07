import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from dpMonitor import Watcher, upload_file
import os
import json
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("DocuBase Folder Watchdog")
        self.root.geometry("400x300")
        
        self.directory_to_watch = tk.StringVar()
        self.ssh_credentials = {"host": "", "port": "", "username": "", "password": ""}
        self.create_widgets()
        self.load_ssh_credentials()  # Load credentials from file and verify
        self.print_credentials_directory()  # Print the directory where credentials are saved

    def create_widgets(self):
        # Create the menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        self.options_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Options", menu=self.options_menu)
        self.options_menu.add_command(label="Set SSH Credentials", command=self.open_ssh_credentials_dialog)
        self.options_menu.add_command(label="Check SSH Credentials", command=self.verify_ssh_credentials)
        
        ttk.Label(self.root, text="Directory to Watch: ").pack(pady=5)
        self.directory_entry = ttk.Entry(self.root, textvariable=self.directory_to_watch, width=40)
        self.directory_entry.pack(pady=5)
        
        self.select_folder_btn = ttk.Button(self.root, text="Select Folder", command=self.browse_directory)
        self.select_folder_btn.pack(pady=5)
        self.start_button = ttk.Button(self.root, text="Start Watchdog", command=self.start_watching)
        self.start_button.pack(pady=5)
        
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory_to_watch.set(directory)
    
    def start_watching(self):
        directory = self.directory_to_watch.get()
        if os.path.isdir(directory):
            self.watcher = Watcher(directory, self.upload_file)
            self.start_button.config(state=tk.DISABLED)
            messagebox.showinfo("Information", "Started watching the directory")
            self.watcher.run()
        else:
            messagebox.showerror("Error", "Invalid Directory")
    
    def upload_file(self, filepath):
        try:
            upload_file(filepath, **self.ssh_credentials)
            print(f"Uploaded: {filepath}")
        except Exception as e:
            print(f"Failed to upload {filepath}: {str(e)}")
    
    def open_ssh_credentials_dialog(self):
        # Create a new top-level window for SSH credentials input
        dialog = tk.Toplevel(self.root)
        dialog.title("SSH Credentials")
        
        tk.Label(dialog, text="Client IP:").grid(row=0, column=0, padx=10, pady=5)
        self.host_entry = tk.Entry(dialog)
        self.host_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Port:").grid(row=1, column=0, padx=10, pady=5)
        self.port_entry = tk.Entry(dialog)
        self.port_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Server Username:").grid(row=2, column=0, padx=10, pady=5)
        self.username_entry = tk.Entry(dialog)
        self.username_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Server Password:").grid(row=3, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(dialog, show='*')
        self.password_entry.grid(row=3, column=1, padx=10, pady=5)
        
        tk.Button(dialog, text="Save", command=self.save_ssh_credentials).grid(row=4, column=0, columnspan=2, pady=10)
    
    def verify_ssh_credentials(self):
        if all(self.ssh_credentials.values()):  # Check if all fields are non-empty
            messagebox.showinfo("Verification", "SSH Credentials have been saved and loaded correctly.")
        else:
            messagebox.showwarning("Verification", "SSH Credentials file is missing or contains incomplete data.")
        print(f"Current SSH Credentials: {self.ssh_credentials}")  # Print credentials to console
    
    def get_app_data_directory(self):
        directory = os.getenv('APPDATA', os.path.expanduser('~'))
        logging.debug(f"App data directory: {directory}")
        return directory
    
    def print_credentials_directory(self):
        directory = self.get_app_data_directory()
        logging.debug(f"SSH Credentials are saved in: {directory}")
        print(f"SSH Credentials are saved in: {directory}")
    
    def load_ssh_credentials(self):
        path = os.path.join(self.get_app_data_directory(), "ssh_credentials.json")
        logging.debug(f"Loading SSH credentials from {path}")
        if os.path.exists(path):
            try:
                with open(path, "r") as file:
                    self.ssh_credentials = json.load(file)
                logging.info("SSH Credentials Loaded Successfully")
            except json.JSONDecodeError:
                logging.error("Error: Failed to decode JSON from SSH credentials file")
                self.ssh_credentials = {"host": "", "port": "", "username": "", "password": ""}
            except Exception as e:
                logging.error(f"Error: {e}")
                self.ssh_credentials = {"host": "", "port": "", "username": "", "password": ""}
        else:
            logging.warning("SSH Credentials file does not exist")
    
    def save_ssh_credentials(self):
        self.ssh_credentials = {
            "host": self.host_entry.get(),
            "port": self.port_entry.get(),
            "username": self.username_entry.get(),
            "password": self.password_entry.get()
        }
        path = os.path.join(self.get_app_data_directory(), "ssh_credentials.json")
        logging.debug(f"Saving SSH credentials to {path}")
        try:
            with open(path, "w") as file:
                json.dump(self.ssh_credentials, file, indent=4)  # Use indent for readability
            logging.info(f"SSH Credentials saved successfully to {path}")
            if os.path.exists(path):
                logging.debug("File exists after saving.")
            else:
                logging.error("File does not exist after saving.")
        except Exception as e:
            logging.error(f"Error saving SSH credentials: {e}")
        messagebox.showinfo("Information", "SSH Credentials have been saved.")
        self.host_entry.master.destroy()
