# Add middleware for logging requests/responses

from queue_mngr import QueueManager
from auth_mngr import AuthorizationManager
from config import load_config
from server import start_app

def run():
    conf = load_config()    # Loads data from the config file
    queue_data = conf['QueueManager']
    
    queue_manager = QueueManager.get_instance(queue_data['path'], queue_data['max_length'], queue_data['save_period_time'])  # Creates a QueueManager instance
    auth_manager = AuthorizationManager()  # Creates an AuthorizationManager instance

    # Ensure required queues exist
    queue_names = queue_manager.list_queue_names()
    if 'transactions' not in queue_names:
        queue_manager.create_queue('transactions')
    if 'results' not in queue_names:
        queue_manager.create_queue('results')

    app = start_app(queue_manager, auth_manager)    # Creates all of the necessary functions for the server app and returns the app
    app.run(host='0.0.0.0', debug=True, port=7500)  # Starts running the server

if __name__ == "__main__":
    run()