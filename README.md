# Distributed Systems Assignment

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

## Framework Choice
gRPC was chosen for its simplicity and performance. The project is split betweeen logical services, AuthenticationService and TransactionService, which gRPC supports naturally clean separation (Service-oriented architecture). It also has built-in authentication support secure communication and token vertification. gRPC is good in speed and efficiency since it uses HTTP/2 and Protocol Buffers for serialization, which ensures faster transmission and reduced payload sizes compared to traditional REST APIs with JSON. 

## Prerequisites

- Python 3.11 or later
- `grpcio` and `protobuf` libraries
- Docker and Docker Compose

## Usage

First install grpcio-tools

```
pip install grpcio-tools
```

Generate gRPC code

```
python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. services.proto
```

Build the Docker image

```
docker build -t grpc:latest .
```

Run the docker container

```
docker run -p 50051:50051 grpc:latest
```

Alternatively, use Docker Compose to start the server and Redis

```
docker-compose up
```

Run the client

```
python client.py
```

## Authors
Leen Al Majzoub
Botond Hernyes