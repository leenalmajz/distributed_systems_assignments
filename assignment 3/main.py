# Add middleware for logging requests/responses

import flask, json, os, yaml
from queue_mngr import QueueManager
from auth_mngr import AuthenticationManager
from config import load_config
from server import start_app

def run():
    conf = load_config()
    queue_data = conf['QueueManager']
    
    queue_manager = QueueManager(queue_data['path'], queue_data['max_length'], queue_data['save_period_time'])
    auth_manager = AuthenticationManager()

    app = start_app(queue_manager, auth_manager)
    app.run(debug=True, port=7500)

if __name__ == "__main__":
    run()