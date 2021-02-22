import time
import subprocess
import sys
import os
import signal
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

class FileModificationHandler(PatternMatchingEventHandler):
    patterns           = ["*.py", "*.pt"]
    current_process    = None
    ignore_directories = False

    def process(self, event):
        print(event.src_path + " was " + event.event_type)
        self.rebuild_and_run()

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

    def on_moved(self, event):
        self.process(event)

    def on_deleted(self, event):
        self.process(event)

    def rebuild_and_run(self):
        print("Restarting...")
        self.kill_current_process()
        print('Running...')
        self.run_process()

    def kill_current_process(self):
        if self.current_process is None:
            return
        try:
            os.kill(self.current_process.pid, signal.SIGTERM)
        except Exception:
            print("Unable to stop current process. Restart this tool.")

    def run_process(self):
        try:
            self.current_process = subprocess.Popen(['python3.7', 'main.py'])
        except Exception as e:
            print("Unable to start process: " + str(e))

def main():
    args = sys.argv[1:]

    observer = Observer()
    handler = FileModificationHandler()
    handler.rebuild_and_run()
    observer.schedule(handler, path=args[0] if args else '.', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == '__main__':
    main()