# Project README

## Overview

This project implements a message queue system with user authentication and authorization. It allows users to create and manage queues, and push and pull messages from them.  The system also includes logging and configuration capabilities.

## File Descriptions

* `auth_mngr.py`: This module defines the `AuthenticationManager` class, which is responsible for managing user authentication tokens. It supports different user roles (BASIC, ADMINISTRATOR, SECRETARY, AGENT) and provides methods for saving, deleting, and authenticating tokens.
* `config.py`: This module provides the `load_config` function, which loads the application's configuration from a YAML file (default: `config.yaml`).
* `main.py`: This is the main entry point of the application. It initializes the `QueueManager` and `AuthenticationManager`, and starts the Flask application defined in `server.py`.
* `models.py`: This module defines the data models used in the application, including `Message`, `Transaction`, `Result`, and `User` classes.  These classes represent the structure of the data being stored and exchanged.
* `queue_mngr.py`: This module defines the `QueueManager` class, which manages the message queues. It provides methods for creating, listing, deleting queues, and pushing and pulling messages.  It also handles saving queue data to a file.
* `server.py`: This module defines the Flask application and its routes. It handles API requests for managing queues and messages, and includes authentication and authorization checks.  It also includes logging of requests and responses.

## Configuration

The application's configuration is loaded from a YAML file (default: `config.yaml`).  The configuration file should contain the following:

* `QueueManager`:
    * `path`: The path to the file where queue data is stored.
    * `max_length`: The maximum length of each queue.
    * `save_period_time`: The time interval (in seconds) for periodically saving queue data to the file.

## Dependencies

The project requires the following Python packages:

* Flask
* PyYAML

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