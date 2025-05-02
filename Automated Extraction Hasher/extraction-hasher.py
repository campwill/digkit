import os
import hashlib
import time
import sys
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

directory = "C:\\directory\\to\\monitor"

class ZipFileEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        filename = os.path.basename(event.src_path)
        if filename.endswith('.zip'):
            time.sleep(5)
            if os.path.isfile(event.src_path):
                calculate_sha256(event.src_path)


def calculate_sha256(filename):
    with open(filename, 'rb') as file:
        file_data = file.read()
        sha256_hash = hashlib.sha256(file_data).hexdigest()

        name = "Hash for " + os.path.basename(filename) + ".txt"
        with open(os.path.join(os.path.dirname(filename),name),'w') as fp:
            fp.write(sha256_hash)


if __name__ == "__main__":
    event_handler = ZipFileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path=directory, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()