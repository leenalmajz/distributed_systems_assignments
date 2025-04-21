# Distributed Systems Assignments

This project implements a gRPC-based distributed system with authentication and transaction services. It includes a server, client, and Docker setup for deployment.

## Features

### Authentication Service
- Add, update, and delete users.
- Authenticate users with username and password.
- Verify user tokens.

### Transaction Service
- Add, update, and delete transactions.
- Add, update, and delete results.
- Fetch all transactions or transactions of a specific user.
- Fetch results of a specific transaction.

## Project Structure
├── client.py # gRPC client implementation 
├── server.py # gRPC server implementation 
├── services.proto # Protocol Buffers definition 
├── services_pb2.py # Generated Python code from .proto 
├── services_pb2_grpc.py # Generated gRPC code from .proto 
├── Dockerfile # Dockerfile for containerizing the server 
├── docker-compose.yml # Docker Compose file for multi-container setup 
├── requirements.txt # Python dependencies 
└── README.md # Project documentation


## Prerequisites

- Python 3.11 or later
- `grpcio` and `protobuf` libraries
- Docker and Docker Compose

## Setup

### 1. Install Dependencies
Install the required Python dependencies:
```bash
pip install -r [requirements.txt](http://_vscodecontentref_/9)