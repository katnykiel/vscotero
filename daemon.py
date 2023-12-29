# daemon.py
# runs in the background and checks for changes in the user-provided .bib file

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class FileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f'File {event.src_path} has been modified')
            # TODO: Add script executable here

def check(watchdog_path):
    path = watchdog_path
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()