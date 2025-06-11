import json, time, os

# We had to change this file a bit so that we could implement mpi and docker, but the main concept of how it works is pretty much the same.
class QueueManager:
    _instances = {} # Store instances by path to ensure singleton per queue file

    def __init__(self, path, max_length, save_period_time):
        self.path = path    # These values are loaded from the config file
        self.max_length = max_length
        self.save_period_time = save_period_time    # in seconds
        self.last_save_time = time.time()
        self.queues = self.load_from_file()

    @classmethod
    def get_instance(cls, path, max_length, save_period_time) -> 'QueueManager':    
        # Makes sure only one queue manager is created. For some reason we had a problem that multiple queue managers existed at the same time.
        if path not in cls._instances:
            cls._instances[path] = cls(path, max_length, save_period_time)
        return cls._instances[path]

    def load_from_file(self):
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

    def save_to_file(self):
        try:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            with open(self.path, 'w') as f:
                json.dump(self.queues, f, indent=2)
            self.last_save_time = time.time()
        except Exception as e:
            print(f"Error saving queue data to {self.path}: {e}")

    def create_queue(self, queue_name: str):
        '''
        Creates an empty queue with the name given as the parameter
        '''
        self.queues = self.load_from_file()
        if queue_name not in self.queues:
            self.queues[queue_name] = []
            self.save_to_file()
            print(f"Queue '{queue_name}' created successfully.")
            return True
        else:
            print(f"Queue '{queue_name}' already exists.")
            return False

    def list_queue_content(self, queue_name):
        '''
        Returns the content of a queue specified by it's name
        '''
        self.queues = self.load_from_file()
        if queue_name not in self.queues.keys():
            return False
        return self.queues[queue_name] 
        
    def list_queue_names(self):
        '''
        Returns a list of the available queue names
        '''
        self.queues = self.load_from_file()
        return self.queues.keys()

    def delete_queue(self, queue_name):
        '''
        Deletes a queue from the queues list specified by it's name
        '''
        self.queues = self.load_from_file()
        if queue_name in self.queues.keys():
            self.queues.pop(queue_name)
            self.save_to_file()
            return True
        return False

    def push(self, queue_name: str, content):
        '''
        Appends a message at the end of the specified queue
        '''
        self.queues = self.load_from_file()
        if queue_name not in self.queues:
            print(f"Queue '{queue_name}' doesn't exist")
            return False

        if len(self.queues[queue_name]) >= self.max_length:
            print(f"Queue '{queue_name}' is full. Message not pushed.")
            return False

        message_payload = content.body if hasattr(content, 'body') else content
        self.queues[queue_name].append(message_payload)
        self.save_to_file()
        return True

    def pull(self, queue_name: str):
        '''
        Removes and returns a message from the start of the specified queue
        '''
        self.queues = self.load_from_file()
        if self.queues[queue_name] is None or not isinstance(self.queues[queue_name], list) or len(self.queues[queue_name]) <= 0:
            return None

        message_body = self.queues[queue_name].pop(0)
        self.save_to_file()
        return message_body