from typing import Dict
import threading, pathlib, json, time, atexit, collections
from models import Message

class QueueManager():
    index = 0
    def __init__(self, path: str, max_length: int, save_period_time: int):
        QueueManager.index += 1
        if QueueManager.index > 1:  # Makes sure only one queue manager is created. For some reason we had a problem that multiple queue managers existed at the same time.
            return
        self.file = pathlib.Path(path)  # These values are loaded from the config file
        self.max_length = max_length
        self.queues: Dict[str, collections.deque] = {}

        self.save_period_time = save_period_time  # in seconds
        self.thread_lock = threading.Lock() # We need a lock in case the program wanted to access the persistent storage twice at the same time

        if self.file.exists():
            with self.file.open() as f:
                cont = json.load(f)
                for queue_name, queue_content in cont.items():
                    self.queues.update({queue_name: collections.deque(queue_content, maxlen = self.max_length)})

        t = threading.Thread(target=self.periodical_save)   # setting up a thread to run a periodical save simultaneously to everything else
        t.start()   
        atexit.register(self.save_to_file)  # Save the file when the server stops

    def save_to_file(self):
        '''
        Saves the queues and their content into a json file
        '''
        if len(self.queues) == 0:
            return
        with self.thread_lock:
            cont = {}
            for queue_name, queue_content in self.queues.items():
                cont.update({queue_name: list(queue_content)})
            with self.file.open(mode = "w") as f:
                json.dump(cont, f)
            print("File saved")

    def periodical_save(self):
        '''
        Periodically calls the save_to_file function
        '''
        while True:
            time.sleep(self.save_period_time)
            self.save_to_file()

    def create_queue(self, queue_name):
        '''
        Creates an empty queue with the name given as the parameter
        '''
        with self.thread_lock:
            if queue_name not in self.queues.keys():
                self.queues.update({queue_name: collections.deque(maxlen = self.max_length)})
                return True
            return False

    def list_queue_content(self, queue_name):
        '''
        Returns the content of a queue specified by it's name
        '''
        with self.thread_lock:
            if queue_name not in self.queues.keys():
                return False
            return self.queues[queue_name] 
        
    def list_queue_names(self):
        '''
        Returns a list of the available queue names
        '''
        with self.thread_lock:
            return self.queues.keys()

    def delete_queue(self, queue_name):
        '''
        Deletes a queue from the queues list specified by it's name
        '''
        with self.thread_lock:
            if queue_name in self.queues.keys():
                self.queues.pop(queue_name)
                return True
            return False

    def push(self, queue_name, content: Message):
        '''
        Appends a message at the end of the specified queue
        '''
        with self.thread_lock:
            queue = self.queues.get(queue_name)
            if len(queue) >= self.max_length:
                return False
            queue.append(content.body)
            return True

    def pull(self, queue_name):
        '''
        Removes and returns a message from the start of the specified queue
        '''
        with self.thread_lock:
            queue = self.queues.get(queue_name)
            if len(queue) <= 0:
                return None
            return queue.popleft()