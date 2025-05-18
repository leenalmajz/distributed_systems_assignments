from typing import Dict, Any
import threading, pathlib, json, time, atexit

class Storage():
    def __init__(self, path: str, max_length: int, save_period_time: int):
        self.file = pathlib.Path(path)
        self.max_length = max_length
        self.queues: Dict[str, Any] = {}

        self.save_period_time = save_period_time  # in seconds
        self.thread_lock = threading.Lock()

        if self.file.exists():
            with self.file.open() as f:
                cont = json.load(f)
                for queue_name, queue_content in cont.items():
                    self.queues.update({queue_name: queue_content})

        t = threading.Thread(target=self.periodical_save, daemon=True)
        t.start()   
        atexit.register(self.save_to_file)  # Save the file when the server stops

    def save_to_file(self):
        with self.thread_lock:
            cont = {}
            for queue_name, queue_content in self.queues.items():
                cont.update({queue_name: list(queue_content)})
            with self.file.open(mode = "w") as f:
                json.dump(cont, f)

    def periodical_save(self, queue_name):
        while True:
            time.sleep(self.save_period_time)
            self.save_to_file()

    def create_queue(self, queue_name):
        with self.thread_lock:
            if queue_name in self.queues.keys():
                return False
            self.queues
            return True

    def list_queue(self):
        with self.thread_lock:
            return

    def delete_queue(self, queue_name):
        with self.thread_lock:
            return

    def push(self, queue_name, content):
        with self.thread_lock:
            return

    def pull(self, queue_name, content):
        with self.thread_lock:
            return
