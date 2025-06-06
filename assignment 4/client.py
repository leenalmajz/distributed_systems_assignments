#####################
#####################
# THIS FILE IS NOT NECESSARY FOR THE PROGRAM TO WORK
# IT ONLY HAS TESTING PURPOSES
#####################
#####################

import requests

# 1. Login
login_url = "http://localhost:7500/login"
login_data = {"username": "admin", "password": "admin123"}

try:
    response = requests.post(login_url, json=login_data)
    response.raise_for_status()  # Raises an exception for HTTP errors
    token = response.json()["token"]
    print("Token:", token)
except requests.exceptions.RequestException as e:
    print("Request failed:", e)
except ValueError as e:
    print("Invalid JSON response:", e)

# 2. Create a queue
# THIS ALREADY EXISTS IN THE PERSISTENT STORAGE, SO IT WILL GIVE AN ERROR
try:
    queue_name = "transactions"
    headers = {"Authorization": token}
    create_queue_url = f"http://localhost:7500/queues/{queue_name}"
    response = requests.post(create_queue_url, headers=headers)
    print(response.json())
except requests.exceptions.RequestException as e:
    print("Request failed:", e)
except ValueError as e:
    print("Invalid JSON response:", e)


# 3. Push a message
try:
    push_url = f"http://localhost:7500/queues/{queue_name}/messages"
    message = {"transaction_id": "123", "customer": {"user_id": 1, "username": "admin", "password": "admin123", "role": "user"}, "status": 0, "vendor_id": "456", "amount": 100}
    response = requests.post(push_url, json=message, headers=headers)
    print(response.json())
except requests.exceptions.RequestException as e:
    print("Request failed:", e)
except ValueError as e:
    print("Invalid JSON response:", e)

# 4. Pull a message

# first push a new one
try:
    push_url = f"http://localhost:7500/queues/{queue_name}/messages"
    message = {"transaction_id": "124", "customer": {"user_id": 1, "username": "admin", "password": "admin123", "role": "user"}, "status": 1, "vendor_id": "444", "amount": 200}
    response = requests.post(push_url, json=message, headers=headers)
    print(response.json())
except requests.exceptions.RequestException as e:
    print("Request failed:", e)
except ValueError as e:
    print("Invalid JSON response:", e)

try:
    pull_url = f"http://localhost:7500/queues/{queue_name}/messages/first"
    response = requests.get(pull_url, headers=headers)
    print(response.json())
except requests.exceptions.RequestException as e:
    print("Request failed:", e)
except ValueError as e:
    print("Invalid JSON response:", e)