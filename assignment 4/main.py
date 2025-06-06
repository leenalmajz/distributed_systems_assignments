# Add middleware for logging requests/responses

import flask, json, os, yaml
from queue_mngr import QueueManager
from ml_service import MLService
from auth_mngr import AuthorizationManager
from config import load_config
from server import start_app

def run():
    conf = load_config()    # Loads data from the config file
    queue_data = conf['QueueManager']
    
    queue_manager = QueueManager(queue_data['path'], queue_data['max_length'], queue_data['save_period_time'])  # Creates a QueueManager instance
    auth_manager = AuthorizationManager()  # Creates an AuthorizationManager instance

    ml_data = conf['MLModel']
    ml_service = MLService(queue_manager, ml_data['path'], ml_data['num_processors'])

    app = start_app(queue_manager, auth_manager, ml_service)    # Creates all of the necessary functions for the server app and returns the app
    app.run(debug=True, port=7500)  # Starts running the server

if __name__ == "__main__":
    run()