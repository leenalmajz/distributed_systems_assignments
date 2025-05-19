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
    max_length: 100
    save_period_time: 30
```
* 	`path`: File where the state of the queues is stored
*   `max_length`: Max number of messages per queue
*   `save_period_time`: Periodic save interval (in seconds)

## File Descriptions

* `auth_mngr.py`: This module defines the `AuthenticationManager` class, which is responsible for managing and verifying user authentication tokens based on their roles  (BASIC, ADMINISTRATOR, SECRETARY, AGENT) and provides methods for saving, deleting, and authenticating tokens.
* `client.py`: 
* `config.py`: This module provides the `load_config` function, which loads the application's configuration from a YAML file.
* `main.py`: This is the main entry point of the application. It initializes the `QueueManager` and `AuthenticationManager`, and starts the Flask application defined in `server.py` on port 7500.
* `models.py`: This module defines the data models used in the application, including `Message`, `Transaction`, `Result`, and `User` classes, each with methods for serialization and deserialization to support structured data handling and persistence across the system.
* `queue_mngr.py`: This module defines the `QueueManager` class, which manages the message queues. It provides methods for creating, listing, deleting queues, and pushing and pulling messages. It also handles persistence of multiple message queues using thread-safe operations and periodic saving to a file, ensuring durability and controlled queue sizes for a high-performance message processing system.
* `server.py`: This module defines the Flask web server that exposes a secure, token-authenticated REST API for managing message queues and handling different message types (like Transaction and Result), with logging, user roles, and detailed request auditing.


## How to Run

1.  Clone the repository.
2.  Install the dependencies using `pip install -r requirements.txt`.
3.  Run the application using `python main.py`.

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
                "role": "integer"
            }
            ```
* `GET /queues`:
    * Description: Retrieves a list of all queues.
    * Authentication: Requires a valid user token in the `Authorization` header.
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

## Authentication and Authorization

* Users are authenticated using a username and password.  Upon successful login, a token is generated.
* Authorization is role-based.  Different roles (ADMINISTRATOR, AGENT) have different permissions.
* The `AuthenticationManager` class is used to manage tokens and roles.
* The server uses the `Authorization` header to check for tokens.

## Logging

The server logs all requests and responses to `message_queue.log`.  The log includes the source, destination, headers, metadata, and body of each message.

## Conclusion

This message queue system provides a robust, scalable, and secure backend service tailored for HPC machine learning environments. By combining role-based access control, structured message handling, durable queue management, and comprehensive logging, it ensures reliable message delivery and easy maintainability. Whether used in research, production, or predictive analytics workflows, the system is designed to be both flexible and extensible for evolving needs.