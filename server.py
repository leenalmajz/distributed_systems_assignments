""" TODO:
    1. add documentation
    2. add context
    3. add testing"""

import grpc
import secrets
from concurrent import futures
import logging
import services_pb2
import services_pb2_grpc


class AuthenticationService(services_pb2_grpc.AuthenticationServiceServicer):
    users = {}
    current_id = 1

    def authenticate_user(self, username, password):
        if username == "" or password == "":
            return (False, None, 'username or password not given', None, None)

        for user_id, user_dict in self.users.items():
            if user_dict['user'].username == username and user_dict['user'].password == password:
                random_token = secrets.token_urlsafe(64)
                user_dict['token'] = random_token
                return (True, random_token, '', user_dict['user'].role, user_dict['user'])

        return (False, None, 'username or password is incorrect', None, None)

    def Authenticate(self, request, context):
        success, token, error_msg, role, _ = self.authenticate_user(request.username, request.password)
        if success:
            return services_pb2.AuthenticationResponse(success=True, error_message='', role=role, token=token)
        else:
            return services_pb2.AuthenticationResponse(success=False, error_message=error_msg)

    def AddUser(self, request, context):
        if request.user_id == 0:
            request.user_id = self.current_id
            self.current_id += 1

        if request.user_id in self.users:
            return services_pb2.AddUserResponse(success=False, error_message='User already present')

        random_token = secrets.token_urlsafe(64)
        self.users[request.user_id] = {'user': request, 'token': random_token}
        print(f'Added new user with id = {request.user_id} and name {request.username}')
        return services_pb2.AddUserResponse(success=True, error_message='', users=[request])

    def UpdateUser(self, request, context):
        if request.old_user_data.user_id not in self.users:
            return services_pb2.UpdateUserResponse(success=False, error_message='User not present')

        self.users[request.old_user_data.user_id]['user'].username = request.new_user_data.username
        self.users[request.old_user_data.user_id]['user'].password = request.new_user_data.password
        self.users[request.old_user_data.user_id]['user'].role = request.new_user_data.role

        print(f'Updated user with id = {request.old_user_data.user_id} and name {request.new_user_data.username}')
        return services_pb2.UpdateUserResponse(success=True, error_message='', users=[self.users[request.old_user_data.user_id]['user']])

    def DeleteUser(self, request, context):
        if request.user_id not in self.users:
            return services_pb2.DeleteUserResponse(success=False, error_message='User not present')

        user = self.users[request.user_id]['user']
        self.users.pop(request.user_id)
        print(f'Deleted user with id = {request.user_id} and name {user.username}')
        return services_pb2.DeleteUserResponse(success=True, error_message='')

    def VerifyToken(self, request, context):
        if request.token == '':
            return services_pb2.VerifyTokenResponse(success=False, error_message='Token not given')

        if request.user.user_id not in self.users:
            return services_pb2.VerifyTokenResponse(success=False, error_message='User not present')

        user_dict = self.users[request.user.user_id]

        if user_dict['user'] == request.user and user_dict['token'] == request.token:
            return services_pb2.VerifyTokenResponse(success=True)
        return services_pb2.VerifyTokenResponse(success=False, error_message='Token is not valid')

class TransactionService(services_pb2_grpc.TransactionServiceServicer):
    transactions = {}
    results = {}
    current_transaction_id = 1
    current_result_id = 1

    def AddTransaction(self, request, context):
        """
        Adds a transaction if the user is authenticated and authorized.
        """
        auth_service = AuthenticationService()
        success, token, error_msg, role, _ = auth_service.authenticate_user(
            request.user.username,
            request.user.password
        )   

        if not success:
            return services_pb2.AddTransactionResponse(success=False, error_message='User not authenticated')

        # Assign a transaction ID if it's not set
        if request.Transaction.transaction_id == 0:
            request.Transaction.transaction_id = self.current_transaction_id
            self.current_transaction_id += 1

        # Check for duplicate transaction 
        if request.Transaction.transaction_id in self.transactions:
            return services_pb2.AddTransactionResponse(success=False, error_message='Transaction already present')

        # Add the transaction
        self.transactions[request.Transaction.transaction_id] = request.Transaction
        print(f'Added new transaction with id = {request.Transaction.transaction_id}')
        return services_pb2.AddTransactionResponse(success=True, error_message='', transactions=[request.Transaction])

    def UpdateTransaction(self, request, context):
        """
        Updates a transaction if the user is authenticated and authorized.
        """
        auth_service = AuthenticationService()
        success, token, error_msg, role, _ = auth_service.authenticate_user(
            request.user.username,
            request.user.password
        )

        if not success:
            return services_pb2.UpdateTransactionResponse(success=False, error_message='User not authenticated')
        
        # Check if the transaction exists
        if request.old_transaction_data.transaction_id not in self.transactions:
            return services_pb2.UpdateTransactionResponse(success=False, error_message='Transaction not present')

        self.transactions[request.old_transaction_data.transaction_id].status = request.new_transaction_data.status
        self.transactions[request.old_transaction_data.transaction_id].amount = request.new_transaction_data.amount
        self.transactions[request.old_transaction_data.transaction_id].vendor_id = request.new_transaction_data.vendor_id
        self.transactions[request.old_transaction_data.transaction_id].amount = request.new_transaction_data.amount
        print(f'Updated transaction with id = {request.old_transaction_data.transaction_id}')

        return services_pb2.UpdateTransactionResponse(success=True, error_message='', transactions=[self.transactions[request.old_transaction_data.transaction_id]])

    def DeleteTransaction(self, request, context):
        """
        Deletes a transaction if the user is authenticated and authorized.
        """
        auth_service = AuthenticationService()
        success, token, error_msg, role, _ = auth_service.authenticate_user(
            request.user.username,
            request.user.password
        )

        if not success:
            return services_pb2.DeleteTransactionResponse(success=False, error_message='User not authenticated')

        # Check if the transaction exists
        if request.transaction.transaction_id not in self.transactions:
            return services_pb2.DeleteTransactionResponse(success=False, error_message='Transaction not present')

        self.transactions.pop(request.transaction.transaction_id)
        print(f'Deleted transaction with id = {request.transaction.transaction_id}')
        return services_pb2.DeleteTransactionResponse(success=True, error_message='')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    services_pb2_grpc.add_AuthenticationServiceServicer_to_server(AuthenticationService(), server)
    services_pb2_grpc.add_TransactionServiceServicer_to_server(TransactionService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()