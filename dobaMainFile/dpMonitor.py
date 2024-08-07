import paramiko 
import os 
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher: 
    def __init__ (self, directory, upload_callback):
        self.directory = directory
        self.observer = Observer()
        self.upload_callback = upload_callback
        
    def run(self):
        event_handler = Handler(self.upload_callback)
        self.observer.schedule(event_handler, self.directory, recursive=True)
        self.observer.start()
        try:
            while True: 
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop
        self.observer.join()

class Handler(FileSystemEventHandler):
    def __init__(self, upload_callback):
        self.upload_callback = upload_callback
    
    def on_created(self, event):
        if event.is_directory:
            return None
        else:
            self.upload_callback(event.src_path)


def upload_file(filepath):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect()