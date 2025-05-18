from typing import Dict
import threading, pathlib, json, time, atexit, collections

class QueueManager():
    def __init__(self, path: str, max_length: int, save_period_time: int):
        self.file = pathlib.Path(path)
        self.max_length = max_length
        self.queues: Dict[str, collections.deque] = {}

        self.save_period_time = save_period_time  # in seconds
        self.thread_lock = threading.Lock()

        if self.file.exists():
            with self.file.open() as f:
                cont = json.load(f)
                for queue_name, queue_content in cont.items():
                    self.queues.update({queue_name: collections.deque(queue_content, maxlen = self.max_length)})

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
                print("file saved.")

    def periodical_save(self):
        while True:
            time.sleep(self.save_period_time)
            self.save_to_file()

    def create_queue(self, queue_name):
        with self.thread_lock:
            if queue_name not in self.queues.keys():
                self.queues.update({queue_name: collections.deque(maxlen = self.max_length)})
                return True
            return False

    def list_queue_content(self, queue_name):
        with self.thread_lock:
            if queue_name not in self.queues.keys():
                return False
            return self.queues[queue_name] 
        
    def list_queue_names(self):
        with self.thread_lock:
            return self.queues.keys()

    def delete_queue(self, queue_name):
        with self.thread_lock:
            if queue_name in self.queues.keys():
                self.queues.pop(queue_name)
                return True
            return False

    def push(self, queue_name, content):
        with self.thread_lock:
            queue = self.queues.get(queue_name)
            if len(queue) >= self.max_length:
                return False
            queue.append(content)
            return True

    def pull(self, queue_name):
        with self.thread_lock:
            queue = self.queues.get(queue_name)
            if len(queue) <= 0:
                return None
            return queue.popleft()