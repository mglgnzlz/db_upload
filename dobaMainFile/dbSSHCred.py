import os
import json
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class SSHCredentialsManager:
    def __init__(self):
        self.credentials = {"host": "", "port": "", "username": "", "password": ""}
        self.credentials_path = self.get_credentials_path()

    def get_credentials_path(self):
        directory = os.getenv('APPDATA', os.path.expanduser('~'))
        path = os.path.join(directory, "ssh_credentials.json")
        logging.debug(f"SSH Credentials path: {path}")
        return path

    def load_credentials(self):
        logging.debug(f"Loading SSH credentials from {self.credentials_path}")
        if os.path.exists(self.credentials_path):
            try:
                with open(self.credentials_path, "r") as file:
                    self.credentials = json.load(file)
                logging.info("SSH Credentials Loaded Successfully")
            except json.JSONDecodeError:
                logging.error("Error: Failed to decode JSON from SSH credentials file")
                self.credentials = {"host": "", "port": "", "username": "", "password": ""}
            except Exception as e:
                logging.error(f"Error: {e}")
                self.credentials = {"host": "", "port": "", "username": "", "password": ""}
        else:
            logging.warning("SSH Credentials file does not exist")
        return self.credentials

    def save_credentials(self, credentials):
        self.credentials = credentials
        logging.debug(f"Saving SSH credentials to {self.credentials_path}")
        try:
            with open(self.credentials_path, "w") as file:
                json.dump(self.credentials, file, indent=4)  # Use indent for readability
            logging.info(f"SSH Credentials saved successfully to {self.credentials_path}")
        except Exception as e:
            logging.error(f"Error saving SSH credentials: {e}")

    def verify_credentials(self):
        if all(self.credentials.values()):  # Check if all fields are non-empty
            logging.info("SSH Credentials have been saved and loaded correctly.")
            return True
        else:
            logging.warning("SSH Credentials file is missing or contains incomplete data.")
            return False
