import os
import paramiko
import logging
from threading import Thread
from watcher import Watcher

logging.basicConfig(level=logging.DEBUG)

class UploadLogic:
    def __init__(self, ssh_credentials):
        self.ssh_credentials = ssh_credentials

    def start_watcher(self, directory):
        # Run the watcher in a separate thread to avoid blocking the GUI
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
            remote_path = os.path.join(r"/home/imo/upload", os.path.basename(filepath))  # Adjust the remote path as needed
            sftp.put(filepath, remote_path)
            sftp.close()
            transport.close()
            logging.info(f"Successfully uploaded {filepath} to {remote_path}")
        except Exception as e:
            logging.error(f"Error during SSH upload: {e}")
            raise