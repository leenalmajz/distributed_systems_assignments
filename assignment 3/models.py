import json
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
