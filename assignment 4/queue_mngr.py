import json
import os
import time

class QueueManager:
    _instances = {} # Store instances by path to ensure singleton per queue file

    def __init__(self, path, max_length, save_period_time):
        self.path = path
        self.max_length = max_length
        self.save_period_time = save_period_time
        self.last_save_time = time.time()
        self.queues = self._load_from_file()

    @classmethod
    def get_instance(cls, path, max_length, save_period_time):
        if path not in cls._instances:
            cls._instances[path] = cls(path, max_length, save_period_time)
        return cls._instances[path]

    def _load_from_file(self):
        try:
            if os.path.exists(self.path):
                with open(self.path, 'r') as f:
                    data = json.load(f)
                    if not isinstance(data, dict):
                        print(f"Warning: Queue file '{self.path}' contains invalid data (not a dictionary). Initializing empty queues.")
                        return {}
                    return data
            return {}
        except (json.JSONDecodeError, FileNotFoundError, Exception) as e:
            print(f"Error loading queue data from {self.path}: {e}. Initializing empty queues.")
            return {}

    def _save_to_file(self):
        try:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            with open(self.path, 'w') as f:
                json.dump(self.queues, f, indent=2)
            self.last_save_time = time.time()
        except Exception as e:
            print(f"Error saving queue data to {self.path}: {e}")

    # --- NEW METHOD ADDED ---
    def create_queue(self, queue_name: str):
        """
        Explicitly creates an empty queue with the given name if it doesn't already exist.
        This will ensure the queue is initialized in the persistent storage.
        """
        # Ensure we're working with the latest state from disk
        self.queues = self._load_from_file()

        if queue_name not in self.queues:
            self.queues[queue_name] = []
            self._save_to_file() # Save immediately to persist the new empty queue
            print(f"Queue '{queue_name}' created successfully.")
        else:
            print(f"Queue '{queue_name}' already exists.")
        return True # Indicate success (queue is either created or already exists)
    # --- END NEW METHOD ---

    def push(self, queue_name: str, content):
        self.queues = self._load_from_file()

        if queue_name not in self.queues:
            # If `create_queue` isn't called explicitly, ensure it's a list here
            self.queues[queue_name] = [] 

        message_payload = content.body if hasattr(content, 'body') else content

        if len(self.queues[queue_name]) >= self.max_length:
            print(f"Queue '{queue_name}' is full. Message not pushed.")
            return False

        self.queues[queue_name].append(message_payload)
        self._save_to_file()
        return True

    def pull(self, queue_name: str):
        self.queues = self._load_from_file()
        
        queue = self.queues.get(queue_name)

        if queue is None or not isinstance(queue, list) or len(queue) <= 0:
            return None

        message_body = queue.pop(0)
        self._save_to_file()
        return message_body