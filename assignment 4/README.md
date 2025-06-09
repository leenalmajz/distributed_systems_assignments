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
    path: "queues.json"
    max_length: 999
    save_period_time: 20
```
* 	`path`: File where the state of the queues is stored
*   `max_length`: Max number of messages per queue
*   `save_period_time`: Periodic save interval (in seconds)

```yaml
MLService:
    path: "fraud_rf_model.pkl"
```
* 	`path`: Path where the random forest model is located

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
| `ml_service.py` |	Implements distributed ML prediction using MPI. Handles transaction distribution to workers and result aggregation. Works with both Docker and native MPI environments. |
| `Dockerfile`    | Configures a container with MPI and Python dependencies for reliable distributed execution.
| `docker-compose.yml` | Orchestrates a cluster with 1 master + 4 workers by default, with configurable scaling.
| `fraud_rf_model.pkl` | Pre-trained Random Forest model for fraud detection (should be placed in project root).


## Module Interactions

*   `AuthorizationManager` is used by the API layer `server.py` to validate users before they perform queue operations.
*   `QueueManager` handles all queue-related operations, and is also initialized in `main.py`. It loads data from disk at startup and saves it periodically.
*   `models.py` is used by both `QueueManager` and the API layer to ensure messages conform to structure and can be persisted easily.
*   Logging is handled centrally in the Flask server, capturing all request metadata, headers, and bodies for auditing.
*   `MLService` uses the pre-trained model to predict whether the transactions in the queue are fraudulent or not. It uses separate processes to determine the results more efficiently.

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
                "result": "Queue {queue_name} created"
            }
            ```
* `DELETE /queues/<queue_name>`:
    * Description: Deletes the queue with the specified name.
    * Authentication: Requires a valid administrator token in the `Authorization` header.
    * Response:
        * Body:

            ```json
            {
                "result": "Queue {queue_name} deleted"
            }
            ```
* `POST /queues/<queue_name>/messages`:
    * Description: Adds a message to the specified queue.
    * Request Body (e.g. for adding transaction data):

        ```json
        {
            "transaction_id": "string",
            "customer": {
                "user_id": 1, 
                "username": "string", 
                "password": "string", 
                "role": "string"
            },
            "status": 0, 
            "vendor_id": "string", 
            "amount": 100
        }
        ```
    * Response:
        * Body:

            ```json
            {
                "result": "Message added to queue"
            }
            ```
* `GET /queues/<queue_name>/messages/first`:
    * Description: Retrieves and removes the first message from the specified queue.
    * Authentication: Requires a valid user token in the `Authorization` header.
    * Response:
        * Body:

            ```json
            {
                "transaction_id": "string",
                "customer": {
                    "user_id": 1, 
                    "username": "string", 
                    "password": "string", 
                    "role": "string"
                },
                "status": 0, 
                "vendor_id": "string", 
                "amount": 100
            }
            ```
        Response if there are no more messages in the queue:
        * Body:

            ```json
            {
                "response": "Queue is empty"
            }
            ```

## Description of MLService

**Purpose**:  
Distributed fraud prediction service that processes transactions in parallel using MPI, integrating with the existing message queue system.

**Workflow**:
1. **Initialization**:
   - Loads `fraud_rf_model.pkl` on startup
   - Spawns worker processes (configurable count)
   - Starts threading

2. **Processing Loop**:
   ```plaintext
   [Master Process]
   1. Pulls transactions from queue (max batch = worker count)
   2. Distributes to workers via MPI
   3. Aggregates predictions
   4. Pushes results to results queue
   
   [Worker Processes]
   1. Receive transactions via MPI
   2. Run fraud prediction using loaded model
   3. Return confidence scores to master
   ```

**Communication**:
- **With Queue System**:
  - Reads from `/queues/transactions` (existing endpoint)
  - Writes to `/queues/results` (new endpoint)

- **With Docker**:
  - Each container runs as isolated MPI node
  - Automatic networking between containers via `mpi_network`


## How to Run WITHOUT docker (not recommended)

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

4.  Run MPI
```bash
mpirun -np 5  python ml_service.py
```

### How to test (Optional)

Run in a different terminal 

```bash
python client.py
```

## How to Run WITH docker

1.  Download and open the zip file
2.  Install the dependencies  

```bash
pip install -r requirements.txt
```

3.  Build the docker container
```bash
docker compose up --build -d
```

### How to test (Optional)

Run in a different terminal 

```bash
python client.py
```

Also, you can go to http://localhost:15672/ and use 'guest' for both username and password to test the app with rabbitmq


## Conclusion

This message queue system provides a robust, scalable, and secure backend service tailored for HPC machine learning environments. By combining role-based access control, structured message handling, durable queue management, and comprehensive logging, it ensures reliable message delivery and easy maintainability. Whether used in research, production, or predictive analytics workflows, the system is designed to be both flexible and extensible for evolving needs.