import requests
import time

# Base URL for the queue service
BASE_URL = "http://localhost:7500"
TRANSACTIONS_QUEUE_NAME = "transactions"
RESULTS_QUEUE_NAME = "results"

# Global token for authentication
token = None
headers = {}

def login(username, password):
    global token, headers
    login_url = f"{BASE_URL}/login"
    login_data = {"username": username, "password": password}
    try:
        response = requests.post(login_url, json=login_data)
        response.raise_for_status()
        token = response.json()["token"]
        headers["Authorization"] = token
        print(f"Logged in successfully. Token: {token[:10]}...")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Login failed: {e}")
    except ValueError as e:
        print(f"Invalid JSON response during login: {e}")
    return False

def create_queue(queue_name):
    create_queue_url = f"{BASE_URL}/queues/{queue_name}"
    try:
        response = requests.post(create_queue_url, headers=headers)
        if response.status_code == 200:
            print(f"Queue '{queue_name}' created successfully.")
        elif response.status_code == 409:
            print(f"Queue '{queue_name}' already exists.")
        else:
            response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Failed to create queue '{queue_name}': {e}")
    except ValueError as e:
        print(f"Invalid JSON response during queue creation: {e}")
    return False

def push_message(queue_name, message):
    push_url = f"{BASE_URL}/queues/{queue_name}/messages"
    try:
        response = requests.post(push_url, json=message, headers=headers)
        response.raise_for_status()
        print(f"Pushed message to '{queue_name}': {response.json()}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Failed to push message to '{queue_name}': {e}")
    except ValueError as e:
        print(f"Invalid JSON response during push: {e}")
    return False

def pull_message(queue_name):
    pull_url = f"{BASE_URL}/queues/{queue_name}/messages/first"
    try:
        response = requests.get(pull_url, headers=headers)
        response.raise_for_status()
        
        message = response.json()

        print(f"Pulled raw message from '{queue_name}': {message} (type: {type(message)})") 

        if not message: # Handle empty dict, empty list, None, etc.
            print(f"No valid message content received from '{queue_name}'.")
            return None
        
        return message
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404 or e.response.status_code == 500: # Queue empty or not found (The error is noticed in server.py and handled there)
            return None
        print(f"HTTP error pulling from '{queue_name}': {e}")   # If there is a different error that was not explicitly handled in server.py
        return None
    except requests.exceptions.RequestException as e:   # When the request somehow failed
        print(f"Request failed pulling from '{queue_name}': {e}")
        return None
    except ValueError as e: # When the returned message is somehow incorrect
        print(f"Invalid JSON response (could not parse) pulling from '{queue_name}': {e}")
        return None

def pull_results(messages_to_push):
        print("\n--- Pulling Results from Results Queue ---")
        # 4. Pull messages from the results queue and display worker info
        pulled_count = 0 
        max_pulls = len(messages_to_push) + 6
        tries = 0
        
        while pulled_count < max_pulls or tries > 4:
            try:
                result_message = pull_message(RESULTS_QUEUE_NAME)
                if result_message is not None: # Explicitly check for None
                    if isinstance(result_message, dict):
                        result_id = result_message.get('result_id', 'N/A')
                        transaction_id = result_message.get('transaction_id', 'N/A')
                        is_fraudulent = result_message.get('is_fraudulent', 'N/A')
                        confidence = result_message.get('confidence', 'N/A')
                        
                        print(f"Result ID: {result_id}")
                        print(f"  Transaction ID: {transaction_id}")
                        print(f"  Is Fraudulent: {is_fraudulent}")
                        print(f"  Confidence: {confidence}")
                    else:
                        print(f"Pulled result message has unexpected format (not a dict): {result_message} (type: {type(result_message)})")
                    pulled_count += 1
                else: # result_message is None
                    tries += 1
                    print("No more results in the queue. Waiting for a moment...")
                    time.sleep(2)
                    if pulled_count == len(messages_to_push):
                        print("All pushed messages seem to have been processed and pulled.")
                        break
                    elif pulled_count > len(messages_to_push) * 1.5:
                        print("Exceeded reasonable number of pull attempts without new results. Stopping.")
                        break
            except Exception as e:
                print(e)

if __name__ == "__main__":
    # 1. Login
    if not login("admin", "admin123"):
        exit("Failed to log in. Exiting.")

    # 2. Create transactions queue (optional, as it's assumed to exist)
    create_queue(TRANSACTIONS_QUEUE_NAME)
    create_queue(RESULTS_QUEUE_NAME)

    # 3. Push a few messages to the transactions queue
    print("\n--- Pushing Transactions ---")
    messages_to_push = [
        {"transaction_id": "1", "customer": {"user_id": 101, "username": "userA", "password": "dummy_password", "role": "basic"}, "status": 0, "vendor_id": "11", "amount": 100.0},
        {"transaction_id": "2", "customer": {"user_id": 102, "username": "userB", "password": "dummy_password", "role": "basic"}, "status": 0, "vendor_id": "12", "amount": 550.0},
        {"transaction_id": "3", "customer": {"user_id": 103, "username": "userC", "password": "dummy_password", "role": "basic"}, "status": 0, "vendor_id": "13", "amount": 120.5},
        {"transaction_id": "4", "customer": {"user_id": 104, "username": "userD", "password": "dummy_password", "role": "basic"}, "status": 0, "vendor_id": "14", "amount": 90.0},
        {"transaction_id": "5", "customer": {"user_id": 105, "username": "userE", "password": "dummy_password", "role": "basic"}, "status": 0, "vendor_id": "15", "amount": 2000.0},
        {"transaction_id": "6", "customer": {"user_id": 106, "username": "userF", "password": "dummy_password", "role": "basic"}, "status": 0, "vendor_id": "16", "amount": 300.0},
    ]
    for msg in messages_to_push:
        push_message(TRANSACTIONS_QUEUE_NAME, msg) 
        time.sleep(0.1)

    # 4. Pulling results from the results queue. 
    # In case you want to seee the results in the queues (not for just a split second), comment the next line out!
    pull_results(messages_to_push)
    print("\n--- Client finished ---")