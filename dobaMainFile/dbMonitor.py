import os
import paramiko
import logging
from threading import Thread
from watcher import Watcher
from tkinter import messagebox

logging.basicConfig(level=logging.DEBUG)

class UploadLogic:
    def __init__(self, ssh_credentials):
        self.ssh_credentials = ssh_credentials

    def start_watcher(self, directory):
        self.watcher = Watcher(directory, self.upload_file)
        self.watcher_thread = Thread(target=self.watcher.run)
        self.watcher_thread.daemon = True  # This will allow the thread to exit when the main program exits
        self.watcher_thread.start()


    def upload_file(self, filepath):
        if filepath.lower().endswith('.pdf'):
            try:
                self.ssh_upload(filepath)
                print(f"Uploaded: {filepath}")
            except Exception as e:
                print(f"Failed to upload {filepath}: {str(e)}")
        else:
            logging.info(f"Skipped non-PDF file: {filepath}")

    def ssh_upload(self, filepath):
        logging.debug(f"Initiating SSH connection to {self.ssh_credentials['host']}")
        try:
            transport = paramiko.Transport((self.ssh_credentials["host"], int(self.ssh_credentials["port"])))
            transport.connect(username=self.ssh_credentials["username"], password=self.ssh_credentials["password"])

            sftp = paramiko.SFTPClient.from_transport(transport)

            # Ensure the remote path uses forward slashes (Unix style)
            remote_directory = self.ssh_credentials["folderdestination"]
            remote_path = os.path.join(remote_directory, os.path.basename(filepath)).replace('\\', '/')
            
            sftp.put(filepath, remote_path)
            sftp.close()
            transport.close()
            logging.info(f"Successfully uploaded {filepath} to {remote_path}")
        except Exception as e:
            logging.error(f"Error during SSH upload: {e}")
            raise

