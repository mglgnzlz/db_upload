import os
import logging
import time

class Watcher:
    def __init__(self, directory_to_watch, callback):
        self.directory_to_watch = directory_to_watch
        self.callback = callback
        self.observed_files = set(os.listdir(directory_to_watch))

    def run(self):
        logging.info(f"Starting to watch {self.directory_to_watch}")
        while True:
            time.sleep(1)
            current_files = set(os.listdir(self.directory_to_watch))
            new_files = current_files - self.observed_files
            if new_files:
                for file in new_files:
                    filepath = os.path.join(self.directory_to_watch, file)
                    self.callback(filepath)
            self.observed_files = current_files
