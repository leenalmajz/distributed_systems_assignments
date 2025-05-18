"""This file runs the server and handles the endpoints for the API."""

import os
import json
from flask import Flask, request, jsonify, abort
from models import Message, User, Transaction, Result  # Import your classes
import threading
import time
import logging
from datetime import datetime
from queue_mngr import Storage  # Import the Storage class

# Configuration
MAX_QUEUE_SIZE = 1000  # Default max queue size
PERSISTENCE_INTERVAL = 60  # Default persistence interval in seconds
STORAGE_FILE = "message_queue_storage.json"  # Default storage file
LOG_FILE = "message_queue.log"

# Load configuration from a file (if it exists)
config_file = "config.json"
if os.path.exists(config_file):
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
            MAX_QUEUE_SIZE = config.get("max_queue_size", MAX_QUEUE_SIZE)
            PERSISTENCE_INTERVAL = config.get("persistence_interval", PERSISTENCE_INTERVAL)
            STORAGE_FILE = config.get("storage_file", STORAGE_FILE)
            LOG_FILE = config.get("log_file", LOG_FILE)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {config_file}. Using default configuration.")

# Logging setup
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
def log_message(source, destination, headers=None, metadata=None, body=None):
    """
    Logs a message with detailed information.
    """
    log_entry = {
        "source": source,
        "destination": destination,
        "headers": headers,
        "metadata": metadata,
        "body": body,
    }
    logging.info(json.dumps(log_entry))


app = Flask(__name__)
queue_manager = Storage(path=STORAGE_FILE, max_length=MAX_QUEUE_SIZE, save_period_time=PERSISTENCE_INTERVAL)

def get_user_from_request():
    """
    Helper function to extract user information from the request headers.
    Returns:
        User: The user object, or None if the user cannot be authenticated.
    """
    # TODO: Implement authentication logic here.

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None  # TODO: Handle missing auth header

    #  Extract user data from the header.
    try:
        token_data = json.loads(auth_header)
        user = User(
            user_id=token_data["user_id"],
            username=token_data["username"],
            password="password123",
            role=token_data["role"],
        )
        return user
    except json.JSONDecodeError:
        return None  # TODO: Handle invalid token data

def check_admin_role(user):
    """
    Helper function to check if the user has the administrator role.
    """
    return user and user.role == User.Role.ADMINISTRATOR

def check_agent_role(user):
    """
    Helper function to check if the user has the agent role.
    """
    return user and (user.role == User.Role.AGENT or user.role == User.Role.ADMINISTRATOR)

def get_timestamp():
    """
    Helper function to get the current timestamp in ISO format.
    """
    return datetime.utcnow().isoformat()

##################################################
#_____________________Routes_____________________#
##################################################

@app.route('/queues', methods=['GET'])
def list_queues():
    """
    Lists all queues.
    """
    user = get_user_from_request()
    if not user:
        log_message(source=request.remote_addr, destination="/queues", headers=request.headers, body=None)
        abort(401)
    log_message(source=request.remote_addr, destination="/queues", headers=request.headers, body=None)

    return jsonify(list(queue_manager.queues.keys())), 200

@app.route('/queues/<string:queue_name>', methods=['POST'])
def create_queue(queue_name):
    """
    Creates a new queue.
    """
    user = get_user_from_request()
    if not user:
        log_message(source=request.remote_addr, destination=f"/queues/{queue_name}", headers=request.headers, body=None)
        abort(401)
    if not check_admin_role(user):
        log_message(source=request.remote_addr, destination=f"/queues/{queue_name}", headers=request.headers, body=None)
        abort(403)
    if queue_manager.create_queue(queue_name):
        log_message(source=request.remote_addr, destination=f"/queues/{queue_name}", headers=request.headers, body=None)
        return jsonify({'message': f'Queue {queue_name} created'}), 201
    else:
        log_message(source=request.remote_addr, destination=f"/queues/{queue_name}", headers=request.headers, body=None)
        return jsonify({'error': 'Queue already exists'}), 409

@app.route('/queues/<string:queue_name>', methods=['DELETE'])
def delete_queue(queue_name):
    """
    Deletes a queue.
    """
    user = get_user_from_request()
    if not user:
        log_message(source=request.remote_addr, destination=f"/queues/{queue_name}", headers=request.headers, body=None)
        abort(401)
    if not check_admin_role(user):
        log_message(source=request.remote_addr, destination=f"/queues/{queue_name}", headers=request.headers, body=None)
        abort(403)
    if queue_name not in queue_manager.queues:
        log_message(source=request.remote_addr, destination=f"/queues/{queue_name}", headers=request.headers, body=None)
        return jsonify({'error': 'Queue not found'}), 404
    queue_manager.delete_queue(queue_name)
    log_message(source=request.remote_addr, destination=f"/queues/{queue_name}", headers=request.headers, body=None)
    return jsonify({'message': f'Queue {queue_name} deleted'}), 200

@app.route('/queues/<string:queue_name>/messages', methods=['POST'])
def push_message(queue_name):
    """
    Adds a message to the queue.
    """
    user = get_user_from_request()
    if not user:
        log_message(source=request.remote_addr, destination=f"/queues/{queue_name}/messages", headers=request.headers, body=request.get_json())
        abort(401)
    if not check_agent_role(user):
        log_message(source=request.remote_addr, destination=f"/queues/{queue_name}/messages", headers=request.headers, body=request.get_json())
        abort(403)

    message_data = request.get_json()
    if not message_data:
        log_message(source=request.remote_addr, destination=f"/queues/{queue_name}/messages", headers=request.headers, body=request.get_json())
        return jsonify({'error': 'Invalid message data'}), 400

    # Determine if it is a Transaction or Result message.
    if "transaction_id" in message_data and "customer" in message_data and "status" in message_data:
        try:
            message = Message(body=Transaction.from_dict(message_data).to_dict())
        except Exception as e:
            log_message(source=request.remote_addr, destination=f"/queues/{queue_name}/messages", headers=request.headers, body=request.get_json())
            return jsonify({'error': f'Invalid transaction data: {e}'}), 400
    elif "result_id" in message_data and "transaction_id" in message_data and "timestamp" in message_data:
        try:
            message = Message(body=Result.from_dict(message_data).to_dict())
        except Exception as e:
            log_message(source=request.remote_addr, destination=f"/queues/{queue_name}/messages", headers=request.headers, body=request.get_json())
            return jsonify({'error': f'Invalid result data: {e}'}), 400
    else:
        message = Message(body=message_data) #handles other message types
    if queue_name not in queue_manager.queues:
        log_message(source=request.remote_addr, destination=f"/queues/{queue_name}/messages", headers=request.headers, body=request.get_json())
        return jsonify({'error': 'Queue not found'}), 404
    try:
        queue_manager.push(queue_name, message)
        log_message(source=request.remote_addr, destination=f"/queues/{queue_name}/messages", headers=request.headers, body=request.get_json())
        return jsonify({'message': 'Message added to queue'}), 201
    except ValueError as e:
        log_message(source=request.remote_addr, destination=f"/queues/{queue_name}/messages", headers=request.headers, body=request.get_json())
        return jsonify({'error': str(e)}), 400  #  Return a 400 Bad Request

@app.route('/queues/<string:queue_name>/messages/first', methods=['GET'])
def pull_message(queue_name):
    """
    Removes and returns the first message from the queue.
    """
    user = get_user_from_request()
    if not user:
        log_message(source=request.remote_addr, destination=f"/queues/{queue_name}/messages/first", headers=request.headers, body=None)
        abort(401)
    if not check_agent_role(user):
        log_message(source=request.remote_addr, destination=f"/queues/{queue_name}/messages/first", headers=request.headers, body=None)
        abort(403)
    if queue_name not in queue_manager.queues:
        log_message(source=request.remote_addr, destination=f"/queues/{queue_name}/messages/first", headers=request.headers, body=None)
        return jsonify({'error': 'Queue not found'}), 404
    try:
        message = queue_manager.pull(queue_name)
        log_message(source=request.remote_addr, destination=f"/queues/{queue_name}/messages/first", headers=request.headers, body=None)
        return jsonify(message.to_dict()), 200
    except IndexError:
        log_message(source=request.remote_addr, destination=f"/queues/{queue_name}/messages/first", headers=request.headers, body=None)
        return jsonify({'error': 'Queue is empty'}), 204  #  204 No Content


if __name__ == '__main__':
    app.run(debug=True, port=7500)

