import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from dpMonitor import Watcher, upload_file
import os


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("DocuBase Folder Watchdog")
        self.root.geometry("300x300")
        
        self.directory_to_watch = tk.StringVar()
        self.ssh_credentials = {"host": "", "port": "", "username": "", "password": ""}
        self.create_widgets()
    
    def create_widgets(self):
        # Create the menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        self.options_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Options", menu=self.options_menu)
        self.options_menu.add_command(label="Set SSH Credentials", command=self.open_ssh_credentials_dialog)
        
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
        
        tk.Label(dialog, text="Host:").grid(row=0, column=0, padx=10, pady=5)
        self.host_entry = tk.Entry(dialog)
        self.host_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Port:").grid(row=1, column=0, padx=10, pady=5)
        self.port_entry = tk.Entry(dialog)
        self.port_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Username:").grid(row=2, column=0, padx=10, pady=5)
        self.username_entry = tk.Entry(dialog)
        self.username_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Password:").grid(row=3, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(dialog, show='*')
        self.password_entry.grid(row=3, column=1, padx=10, pady=5)
        
        tk.Button(dialog, text="Save", command=self.save_ssh_credentials).grid(row=4, column=0, columnspan=2, pady=10)
    
    def save_ssh_credentials(self):
        self.ssh_credentials = {
            "host": self.host_entry.get(),
            "port": self.port_entry.get(),
            "username": self.username_entry.get(),
            "password": self.password_entry.get()
        }
        print("SSH Credentials Saved")
        messagebox.showinfo("Information", "SSH Credentials have been saved.")
        self.host_entry.master.destroy()

