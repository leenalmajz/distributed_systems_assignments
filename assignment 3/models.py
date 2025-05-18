import json
from collections import deque
import threading
from datetime import datetime

class Message:
    """
    A class representing a message in the queue.
    """

    def __init__(self, body, metadata=None):
        """
        Initializes a new Message.

        Args:
            body (dict): The message content.
            metadata (dict, optional): Additional metadata.
        Raises:
            TypeError: If body is not a dictionary.
        """
        if not isinstance(body, dict):
            raise TypeError("Message body must be a dictionary")
        self.body = body
        self.metadata = metadata

    def to_dict(self):
        """
        Returns the message as a dictionary.
        Returns:
            dict: A dictionary containing the message body and metadata.
        """
        message_dict = {"body": self.body}
        if self.metadata:
            message_dict["metadata"] = self.metadata
        return message_dict

    def to_json(self):
        """
        Serializes the message to a JSON string.
        Returns:
            str: A JSON string representing the message.
        """
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(json_string):
        """
        Deserializes a JSON string to create a Message object.

        Args:
            json_string (str): A JSON string representing a message.

        Returns:
            Message: A Message object.
        """
        data = json.loads(json_string)
        return Message(data["body"], data.get("metadata"))


class Queue:
    """
    A class representing a message queue.
    """

    def __init__(self, name, max_size=None):
        """
        Initializes a new Queue.

        Args:
            name (str): The name of the queue.
            max_size (int, optional): The maximum size of the queue. Defaults to None (unlimited).
        """
        self.name = name
        self.max_size = max_size
        self._queue = deque()
        self._lock = threading.Lock()

    def push(self, message):
        """
        Adds a message to the end of the queue.

        Args:
            message (Message): The message to add.

        Raises:
            ValueError: If the queue is full (when max_size is set).
            TypeError: If the message is not a Message object.
        """
        with self._lock:
            if not isinstance(message, Message):
                raise TypeError("Message must be a Message object")
            if self.max_size is not None and len(self._queue) >= self.max_size:
                raise ValueError("Queue is full")
            self._queue.append(message)

    def pull(self):
        """
        Removes and returns the first message from the queue.

        Returns:
            Message: The first message in the queue.

        Raises:
            IndexError: If the queue is empty.
        """
        with self._lock:
            if not self._queue:
                raise IndexError("Queue is empty")
            return self._queue.popleft()

    def peek(self):
        """
        Returns the first message without removing it.

        Returns:
            Message: The first message in the queue.

        Raises:
            IndexError: If the queue is empty.
        """
        with self._lock:
            if not self._queue:
                raise IndexError("Queue is empty")
            return self._queue[0]

    def size(self):
        """
        Returns the current number of messages in the queue.

        Returns:
            int: The size of the queue.
        """
        with self._lock:
            return len(self._queue)

    def to_list(self):
        """
        Returns a list of all messages in the queue.

        Returns:
            list: A list of messages (as Message objects).
        """
        with self._lock:
            return [message.to_dict() for message in self._queue]

    def clear(self):
        """
        Removes all messages from the queue.
        """
        with self._lock:
            self._queue.clear()

    def to_dict(self):
        """
        Returns the queue data as a dictionary.

        Returns:
            dict: A dictionary containing the queue's data.
        """
        with self._lock:
            return {
                "name": self.name,
                "max_size": self.max_size,
                "queue": [message.to_dict() for message in self._queue]
            }

    def to_json(self):
        """
        Serializes the queue data to a JSON string.

        Returns:
            str: A JSON string representing the queue's data.
        """
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(json_string):
        """
        Deserializes a JSON string to create a Queue object.

        Args:
            json_string (str): A JSON string representing a queue.

        Returns:
            Queue: A Queue object.
        """
        data = json.loads(json_string)
        queue = Queue(data["name"], data.get("max_size"))
        queue._queue = deque(
            [Message.from_json(json.dumps(msg)) for msg in data.get("queue", [])]
        )
        return queue



class Transaction:
    """
    A class representing a transaction.
    """
    class Status:
        submitted = 0
        accepted = 1
        rejected = 2

    def __init__(self, transaction_id, customer, status, vendor_id, amount):
        self.transaction_id = transaction_id
        self.customer = customer  # This should be a User object.
        self.status = status
        self.vendor_id = vendor_id
        self.amount = amount

    def to_dict(self):
        """
        Returns the transaction as a dictionary
        """
        return {
            "transaction_id": self.transaction_id,
            "customer": self.customer.to_dict(),  # Convert the User object to a dictionary
            "status": self.status,
            "vendor_id": self.vendor_id,
            "amount": self.amount,
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a Transaction object from a dictionary.  Handles the nested User.
        """
        #  Prevent circular import issue.
        from models import User
        customer = User.from_dict(data["customer"])
        return Transaction(
            transaction_id=data["transaction_id"],
            customer=customer,
            status=data["status"],
            vendor_id=data["vendor_id"],
            amount=data["amount"],
        )



class Result:
    """
    A class representing a result.
    """
    def __init__(self, result_id, transaction_id, timestamp, is_fraudulent, confidence):
        self.result_id = result_id
        self.transaction_id = transaction_id
        self.timestamp = timestamp # Store as datetime object
        self.is_fraudulent = is_fraudulent
        self.confidence = confidence

    def to_dict(self):
        """
        Returns the result as a dictionary.  Converts timestamp to ISO format.
        """
        return {
            "result_id": self.result_id,
            "transaction_id": self.transaction_id,
            "timestamp": self.timestamp.isoformat(),
            "is_fraudulent": self.is_fraudulent,
            "confidence": self.confidence,
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a Result object from a dictionary.  Parses the timestamp from ISO format.
        """
        timestamp = datetime.fromisoformat(data["timestamp"])
        return Result(
            result_id=data["result_id"],
            transaction_id=data["transaction_id"],
            timestamp=timestamp,
            is_fraudulent=data["is_fraudulent"],
            confidence=data["confidence"],
        )



class User:
    """
    A class representing a user.
    """
    class Role:
        BASIC = 0
        ADMINISTRATOR = 1
        SECRETARY = 2
        AGENT = 3

    def __init__(self, user_id, username, password, role):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role

    def to_dict(self):
        """
        Returns the user as a dictionary.
        """
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password": self.password,
            "role": self.role,
        }
    @staticmethod
    def from_dict(data):
        """
        Creates a User object from a dictionary.
        """
        return User(
            user_id=data["user_id"],
            username=data["username"],
            password=data["password"],
            role=data["role"],
        )
