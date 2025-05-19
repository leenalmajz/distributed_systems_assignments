# Message Queue System for HPC ML Pipelines
An implementation of a message queue system for secure, durable, and high-performance message processing in machine learning applications.
**Authors:** Leen Al Majzoub, Botond Hernyes

## Introduction

This documentation describes the implementation of a secure and robust message queue system. 

This document is structured as follows:
- We first give a system-level overview.
- Then we outline dependencies and configuration requirements.
- Next, we describe the key modules and their responsibilities.
- We explain how modules interact.
- The API and usage instructions are then presented.
- Finally, we conclude with limitations and reflections.

## Overview of the system

This project implements a message queue system made for high performance computing (HPC) environments, specifically designed to support a machine learning prediction system. The service will allow authenticated agents and administrators to push messages transaction or prediction results into queues and pull them in a FIFO manner. Administrators will have exclusive rights to create and delete queues, with deletion removing all associated messages. The system will enforce a configurable maximum message limit per queue, periodically persist its state to storage for recovery on restart, and handle errors. A configuration file will control key operational parameters, and all client-server interactions will be logged comprehensively, including source, destination, headers, metadata, and message bodies.

We used **Flask** for its lightweight and modular design, and **PyYaml** to manage configuration easily. 

Testing was prioritized early in the development to ensure stability and fast feedback.

## Dependencies and Configuration 
### Required Packages

Install with:

```bash
pip install -r requirements.txt
```

The application's configuration is loaded from a YAML file (default: `config.yaml`).  The configuration file should contain the following:

### Dependecies
* Flask: REST API framework
* PyYAML: For loading the YAML configuration

### Configuration File (config.yaml)
```yaml
QueueManager:
    path: "data/queues.json"
    max_length: 999
    save_period_time: 20
```
* 	`path`: File where the state of the queues is stored
*   `max_length`: Max number of messages per queue
*   `save_period_time`: Periodic save interval (in seconds)

## Module Descriptions

| File            | Description |
|-----------------|-------------|
| `auth_mngr.py`  | Manages authentication and role-based token authorization (`ADMINISTRATOR`, `AGENT`, etc.). Handles token creation and validation. |
| `client.py`     | Simple test client for interacting with the API (used for early testing and debugging). |
| `config.py`     | Loads the YAML configuration file into the application. |
| `main.py`       | Entry point of the application. Initializes and links `AuthorizationManager` and `QueueManager`, and starts the Flask server. |
| `models.py`     | Defines structured data types like `Message`, `Transaction`, `Result`, and `User`, with methods to serialize/deserialize for persistence. |
| `queue_mngr.py` | Core logic for queue handling — includes methods for creation, deletion, pushing/pulling messages, and saving/loading from disk. Thread-safe and supports bounded queues. |
| `server.py`     | Defines all API endpoints, performs request authentication and routing, and integrates logging. Handles both administrative and user-level requests. |


## Module Interactions

*   `AuthorizationManager` is used by the API layer `server.py` to validate users before they perform queue operations.
*   `QueueManager` handles all queue-related operations, and is also initialized in `main.py`. It loads data from disk at startup and saves it periodically.
*   `models.py` is used by both `QueueManager` and the API layer to ensure messages conform to structure and can be persisted easily.
*   Logging is handled centrally in the Flask server, capturing all request metadata, headers, and bodies for auditing.

## API Endpoints

* `POST /login`:
    * Description: Authenticates a user and returns a token.
    * Request Body:

        ```json
        {
            "username": "string",
            "password": "string"
        }
        ```
    * Response:
        * Body:

            ```json
            {
                "token": "string",
                "username": "string",
                "role": "string"
            }
            ```
* `GET /queues`:
    * Description: Retrieves a list of all queues.
    * Authentication: Requires a valid user token in the `Authorization` header.
        * Request Body:

        ```json
        {
            "username": "string",
            "password": "string"
        }
        ```
    * Response:
        * Body:

            ```json
            [
                "queue_name_1",
                "queue_name_2",
                ...
            ]
            ```
* `POST /queues/<queue_name>`:
    * Description: Creates a new queue with the specified name.
    * Authentication: Requires a valid administrator token in the `Authorization` header.
    * Response:
        * Body:

            ```json
            {
                "result": "ok"
            }
            ```
* `DELETE /queues/<queue_name>`:
    * Description: Deletes the queue with the specified name.
    * Authentication: Requires a valid administrator token in the `Authorization` header.
    * Response:
        * Body:

            ```json
            {
                "result": "ok"
            }
            ```
* `POST /queues/<queue_name>/messages`:
    * Description: Adds a message to the specified queue.
    * Request Body:

        ```json
        {
            "body": {
                "key1": "value1",
                "key2": "value2"
            },
            "metadata": {
                "priority": "high",
                "sender": "user1"
            }
        }
        ```
    * Response:
        * Body:

            ```json
            {
                "result": "ok"
            }
            ```
* `GET /queues/<queue_name>/messages/first`:
    * Description: Retrieves and removes the first message from the specified queue.
    * Authentication: Requires a valid user token in the `Authorization` header.
    * Response:
        * Body:

            ```json
            {
                "body": {
                    "key1": "value1",
                    "key2": "value2"
                },
                "metadata": {
                    "priority": "high",
                    "sender": "user1"
                }
            }
            ```
            * Body:
                ```json
               null
                ```


## How to Run

1.  Download and open the zip file
2.  Install the dependencies  

```bash
pip install -r requirements.txt
```

3.  Start the server
```bash
python main.py
```

The server will start on http://localhost:7500.


## How to test


## Conclusion

This message queue system provides a robust, scalable, and secure backend service tailored for HPC machine learning environments. By combining role-based access control, structured message handling, durable queue management, and comprehensive logging, it ensures reliable message delivery and easy maintainability. Whether used in research, production, or predictive analytics workflows, the system is designed to be both flexible and extensible for evolving needs.