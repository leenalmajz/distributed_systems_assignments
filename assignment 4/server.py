import os
import json
from flask import Flask, request, jsonify, abort
from models import Message, User, Transaction, Result  # Import your classes
import threading
import time
import logging
from datetime import datetime
import secrets
from auth_mngr import AuthorizationManager
from queue_mngr import QueueManager
from ml_service import MLService

def start_app(queue_manager: QueueManager, auth_manager: AuthorizationManager):
    app = Flask(__name__)

    #  Dictionary to store tokens for users
    tokens = {}

    LOG_FILE = "message_queue.log"

    # Logging setup
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                        format='%(asctime)s [%(levelname)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    def log_message(source, destination, headers=None, metadata=None, body=None):
        """
        Logs a message with detailed information.
        """
        serializable_headers = dict(headers) if headers else None

        log_entry = {
            "source": source,
            "destination": destination,
            "headers": serializable_headers,
            "metadata": metadata,
            "body": body,
        }
        logging.info(json.dumps(log_entry))
    
    def generate_token(user):
        """Generates a unique token for the given user and stores it."""
        token = secrets.token_urlsafe()
        tokens[user] = token
        
        return token

    def get_user_from_request() -> User | None:
        """
        Helper function to extract user information from the request headers.
        Returns:
            User: The user object, or None if the user cannot be authenticated.
        """

        token_data = request.headers.get("Authorization")
        if not token_data:
            return None

        try:
            for user, token in tokens.items():
                if token == token_data:
                    return user
            return None
        except json.JSONDecodeError:
            return None

    def get_timestamp():
        """
        Helper function to get the current timestamp in ISO format.
        """
        return datetime.utcnow().isoformat()



    ##################################################
    #_____________________Routes_____________________#
    ##################################################

    @app.route('/')
    def home():
        return "ML Service is running", 200
        
    @app.route('/login', methods=['POST'])
    def login():
        """
        Endpoint for user login.
        Handles token generation.
        """
        try:
            data = request.get_json()
            if not data or 'username' not in data or 'password' not in data:
                return jsonify({'error': 'Missing username or password'}), 400

            username = data['username']
            password = data['password']
            
            if username == "test" and password == "password123":
                user = User(user_id=1, username=username, password=password, role="user")
            elif username == "admin" and password == "admin123":
                user = User(user_id=2, username=username, password=password, role="admin")
            elif username == "agent" and password == "agent123":
                user = User(user_id=3, username=username, password=password, role="agent")
            else:
                return jsonify({'error': 'Invalid credentials'}), 401

            token = generate_token(user) # generate token after successful login
            auth_manager.save_token(token, user.role)

            response_data = {
                'token': token,
                'username': username,
                'role': user.role,  # Include the user's role
            }
            log_message(source=request.remote_addr, destination="/login", headers=request.headers, body=data)
            return jsonify(response_data), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500


    @app.route('/queues', methods=['GET'])
    def list_queues():
        """
        Lists all queues.
        """
        user = get_user_from_request()  # gets the user from the header
        if not user:
            log_message(source=request.remote_addr, destination="/queues", headers=request.headers, body=None)
            abort(401)
        log_message(source=request.remote_addr, destination="/queues", headers=request.headers, body=None)

        return jsonify(list(queue_manager.list_queue_names())), 200

    @app.route('/queues/<string:queue_name>', methods=['POST'])
    def create_queue(queue_name):
        """
        Creates a new queue.
        """
        user = get_user_from_request()  # gets the user from the header
        if not user:
            log_message(source=request.remote_addr, destination=f"/queues/{queue_name}", headers=request.headers, body=None)
            abort(401)
        if not auth_manager.auth_admin(tokens[user]):   # Check if the user is authorized (here only admin)
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
        user = get_user_from_request()  # gets the user from the header
        if not user:
            log_message(source=request.remote_addr, destination=f"/queues/{queue_name}", headers=request.headers, body=None)
            abort(401)
        if not auth_manager.auth_admin(tokens[user]):   # Check if the user is authorized (here only admin)
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
        user = get_user_from_request()  # gets the user from the header
        if not user:
            log_message(source=request.remote_addr, destination=f"/queues/{queue_name}/messages", headers=request.headers, body=request.get_json())
            abort(401)
        if not auth_manager.auth_any(tokens[user]):  # Check if the user is authorized (here either admin or agent)
            log_message(source=request.remote_addr, destination=f"/queues/{queue_name}/messages", headers=request.headers, body=request.get_json())
            abort(403)

        message_data = request.get_json()
        if not message_data:
            log_message(source=request.remote_addr, destination=f"/queues/{queue_name}/messages", headers=request.headers, body=request.get_json())
            return jsonify({'error': 'Invalid message data'}), 400

        # Determine if it is a Transaction or a Result message.
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
            message = Message(body=message_data) # if it's some other message type
        if queue_name not in queue_manager.queues:
            log_message(source=request.remote_addr, destination=f"/queues/{queue_name}/messages", headers=request.headers, body=request.get_json())
            return jsonify({'error': 'Queue not found'}), 404
        try:
            queue_manager.push(queue_name, message)
            log_message(source=request.remote_addr, destination=f"/queues/{queue_name}/messages", headers=request.headers, body=request.get_json())
            return jsonify({'message': 'Message added to queue'}), 201
        except ValueError as e:
            log_message(source=request.remote_addr, destination=f"/queues/{queue_name}/messages", headers=request.headers, body=request.get_json())
            return jsonify({'error': str(e)}), 400

    @app.route('/queues/<string:queue_name>/messages/first', methods=['GET'])
    def pull_message(queue_name):
        """
        Removes and returns the first message from the queue.
        """
        user = get_user_from_request()  # gets the user from the header
        if not user:
            log_message(source=request.remote_addr, destination=f"/queues/{queue_name}/messages/first", headers=request.headers, body=None)
            abort(401)

        if not auth_manager.auth_any(tokens[user]):  # Check if the user is authorized (here either admin or agent)
            log_message(source=request.remote_addr, destination=f"/queues/{queue_name}/messages/first", headers=request.headers, body=None)
            abort(403, description="Unauthorized")
        if queue_name not in queue_manager.queues:
            log_message(source=request.remote_addr, destination=f"/queues/{queue_name}/messages/first", headers=request.headers, body=None)
            return jsonify({'error': 'Queue not found'}), 404
        message_body = queue_manager.pull(queue_name)
        if message_body is None:
            log_message(source=request.remote_addr, destination=f"/queues/{queue_name}/messages/first", headers=request.headers, body=None)
            return jsonify({'error': 'Queue is empty'}), 500
        log_message(source=request.remote_addr, destination=f"/queues/{queue_name}/messages/first", headers=request.headers, body=None)
        return jsonify(message_body), 200

    return app

