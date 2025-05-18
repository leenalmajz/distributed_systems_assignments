"""gRPC Server Implementation for Authentication and Transaction Services"""

import grpc
import secrets
import logging
from concurrent import futures
import services_pb2
import services_pb2_grpc

class AuthenticationService(services_pb2_grpc.AuthenticationServiceServicer):
    """
    Provides methods for user management including authentication,
    token verification, addition, update, and deletion.
    """
    users = {}  # In-memory user store: {user_id: {'user': user_obj, 'token': token}}
    current_id = 1  # Auto-incrementing user ID

    def log_info(self, request, context, func_name):
        source = context.peer()
        metadata = context.invocation_metadata()
        request_data = str(request)
    
        print(f"=== [{func_name} Request Log] ===")
        print(f"Source      : {source}")
        print(f"Destination : localhost:50051")
        print(f"Headers     : {metadata}")
        print(f"Message     : {request_data}")
        print("=============================")
    
    def authenticate_user(self, user_id, username, password):
        """
        Validates a user's credentials and generates a token if valid.

        Returns:
            (success: bool, token: str|None, error_msg: str, role: int|None)
        """
        if username == "" or password == "":
            return (False, None, 'username or password not given', None)

        for id, user_dict in self.users.items():
            if id == user_id and user_dict['user'].username == username and user_dict['user'].password == password:
                random_token = secrets.token_urlsafe(64)
                user_dict['token'] = random_token
                return (True, random_token, '', user_dict['user'].role)

        return (False, None, 'username or password is incorrect', None)

    def AddUser(self, request, context):
        """
        Adds a new user to the in-memory user store.

        Returns:
            AddUserResponse: success status and error message if any
        """
        self.log_info(request, context, "AddUser")
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
        """
        Updates existing user data.

        Returns:
            UpdateUserResponse: success status and error message if any
        """
        self.log_info(request, context, "UpdateUser")
        if request.old_user_data.user_id not in self.users:
            return services_pb2.UpdateUserResponse(success=False, error_message='User not present')

        user_record = self.users[request.old_user_data.user_id]['user']
        user_record.username = request.new_user_data.username
        user_record.password = request.new_user_data.password
        user_record.role = request.new_user_data.role

        print(f'Updated user with id = {request.old_user_data.user_id} and name {request.new_user_data.username}')
        return services_pb2.UpdateUserResponse(success=True, error_message='', users=[user_record])

    def DeleteUser(self, request, context):
        """
        Deletes a user by ID.

        Returns:
            DeleteUserResponse: success status and error message if any
        """
        self.log_info(request, context, "DeleteUser")
        if request.user_id not in self.users:
            return services_pb2.DeleteUserResponse(success=False, error_message='User not present')

        user = self.users.pop(request.user_id)['user']
        print(f'Deleted user with id = {request.user_id} and name {user.username}')
        return services_pb2.DeleteUserResponse(success=True, error_message='')

    def Authenticate(self, request, context):
        """
        Authenticates a user and returns a new token.

        Returns:
            AuthenticationResponse: success status, token, error message, and user role
        """
        self.log_info(request, context, "Authenticate")
        success, token, error_msg, role = self.authenticate_user(request.user_id, request.username, request.password)
        return services_pb2.AuthenticationResponse(success=success, error_message=error_msg, role=role if success else 0, token=token or '')

    def VerifyToken(self, request, context):
        """
        Verifies whether a provided token is valid for a given user.

        Returns:
            VerifyTokenResponse: success status
        """
        self.log_info(request, context, "VerifyToken")
        if request.token == '' or request.user.user_id not in self.users:
            return services_pb2.VerifyTokenResponse(success=False)

        user_dict = self.users[request.user.user_id]
        if user_dict['user'] == request.user and user_dict['token'] == request.token:
            return services_pb2.VerifyTokenResponse(success=True)
        
        return services_pb2.VerifyTokenResponse(success=False)


# -------------------------------
# Transaction Service Class
# -------------------------------
class TransactionService(services_pb2_grpc.TransactionServiceServicer):
    """
    Handles transaction and result management including
    creation, modification, deletion, and retrieval.
    """
    transactions = {}  # {transaction_id: {transaction: Transaction}}
    results = {}       # {result_id: {result: Result}}
    current_transaction_id = 1
    current_result_id = 1
    
    def log_info(self, request, context, func_name):
        source = context.peer()
        metadata = context.invocation_metadata()
        request_data = str(request)
    
        print(f"=== [{func_name} Request Log] ===")
        print(f"Source      : {source}")
        print(f"Destination : localhost:50051")
        print(f"Headers     : {metadata}")
        print(f"Message     : {request_data}")
        print("=============================")

    def AddTransaction(self, request, context):
        """
        Adds a new transaction for authorized users.

        Returns:
            AddTransactionResponse: success status, error message, and transaction details
        """
        self.log_info(request, context, "AddTransaction")
        auth_service = AuthenticationService()
        success, token, error_msg, role = auth_service.authenticate_user(request.user.user_id, request.user.username, request.user.password)

        if not success:
            return services_pb2.AddTransactionResponse(success=False, error_message=error_msg)

        if request.user.role not in (1, 3):
            return services_pb2.AddTransactionResponse(success=False, error_message='User not authorized')

        if request.transaction.transaction_id == 0:
            request.transaction.transaction_id = self.current_transaction_id
            self.current_transaction_id += 1

        if request.transaction.transaction_id in self.transactions:
            return services_pb2.AddTransactionResponse(success=False, error_message='Transaction already present')

        self.transactions[request.transaction.transaction_id] = {'transaction': request.transaction}
        print(f'Added new transaction with id = {request.transaction.transaction_id}')
        return services_pb2.AddTransactionResponse(success=True, error_message='', transactions=[request.transaction])

    def UpdateTransaction(self, request, context):
        """
        Updates existing transaction information.

        Returns:
            UpdateTransactionResponse: success status, error message, and updated transaction details
        """
        self.log_info(request, context, "UpdateTransaction")
        auth_service = AuthenticationService()
        success, token, error_msg, role = auth_service.authenticate_user(request.user.user_id, request.user.username, request.user.password)

        if not success or request.user.role not in (1, 3):
            return services_pb2.UpdateTransactionResponse(success=False, error_message=error_msg or 'User not authorized')

        tid = request.old_transaction_data.transaction_id
        if tid not in self.transactions:
            return services_pb2.UpdateTransactionResponse(success=False, error_message='Transaction not present')

        txn = self.transactions[tid]['transaction']
        txn.customer.CopyFrom(request.new_transaction_data.customer)
        txn.status = request.new_transaction_data.status
        txn.vendor_id = request.new_transaction_data.vendor_id
        txn.amount = request.new_transaction_data.amount

        print(f'Updated transaction with id = {tid}')
        return services_pb2.UpdateTransactionResponse(success=True, error_message='', transactions=[txn])

    def DeleteTransaction(self, request, context):
        """
        Deletes a transaction by ID.

        Returns:
            DeleteTransactionResponse: success status and error message if any
        """
        self.log_info(request, context, "DeleteTransaction")
        auth_service = AuthenticationService()
        success, token, error_msg, role = auth_service.authenticate_user(request.user.user_id, request.user.username, request.user.password)

        if not success or request.user.role not in (1, 3):
            return services_pb2.DeleteTransactionResponse(success=False, error_message=error_msg or 'User not authorized')

        tid = request.transaction.transaction_id
        if tid not in self.transactions:
            return services_pb2.DeleteTransactionResponse(success=False, error_message='Transaction not present')

        txn = self.transactions.pop(tid)['transaction']
        print(f'Deleted transaction with id = {tid} and customer: {txn.customer.username}')
        return services_pb2.DeleteTransactionResponse(success=True, error_message='')

    def AddResult(self, request, context):
        """
        Adds a result linked to a transaction.

        Returns:
            AddResultResponse: success status, error message, and result details
        """
        self.log_info(request, context, "AddResult")
        auth_service = AuthenticationService()
        success, token, error_msg, role = auth_service.authenticate_user(request.user.user_id, request.user.username, request.user.password)

        if not success or request.user.role not in (1, 3):
            return services_pb2.AddResultResponse(success=False, error_message=error_msg or 'User not authorized')

        if request.result.transaction_id != request.transaction.transaction_id:
            return services_pb2.AddResultResponse(success=False, error_message='Transaction id mismatch')

        if request.result.transaction_id not in self.transactions:
            return services_pb2.AddResultResponse(success=False, error_message='Transaction not present')

        if request.result.result_id == 0:
            request.result.result_id = self.current_result_id
            self.current_result_id += 1

        if request.result.result_id in self.results:
            return services_pb2.AddResultResponse(success=False, error_message='Result already present')

        self.results[request.result.result_id] = {'result': request.result}
        print(f'Added new result with id = {request.result.result_id}')
        return services_pb2.AddResultResponse(success=True, error_message='', results=[request.result])

    def UpdateResult(self, request, context):
        """
        Updates result data such as fraud status and confidence.

        Returns:
            UpdateResultResponse: success status, error message, and updated result details
        """
        self.log_info(request, context, "UpdateResult")
        auth_service = AuthenticationService()
        success, token, error_msg, role = auth_service.authenticate_user(request.user.user_id, request.user.username, request.user.password)

        if not success or request.user.role not in (1, 3):
            return services_pb2.UpdateResultResponse(success=False, error_message=error_msg or 'User not authorized')

        if request.new_result_data.transaction_id != request.transaction.transaction_id or \
           request.new_result_data.transaction_id not in self.transactions:
            return services_pb2.UpdateResultResponse(success=False, error_message='Transaction not present or mismatch')

        rid = request.old_result_data.result_id
        if rid not in self.results:
            return services_pb2.UpdateResultResponse(success=False, error_message='Result not present')

        result = self.results[rid]['result']
        result.timestamp.CopyFrom(request.new_result_data.timestamp)
        result.is_fraudulent = request.new_result_data.is_fraudulent
        result.confidence = request.new_result_data.confidence
        print(f'Updated result with id = {rid}')
        return services_pb2.UpdateResultResponse(success=True, error_message='', results=[result])

    def DeleteResult(self, request, context):
        """
        Deletes a result by ID.

        Returns:
            DeleteResultResponse: success status and error message if any
        """
        self.log_info(request, context, "DeleteResult")
        auth_service = AuthenticationService()
        success, token, error_msg, role = auth_service.authenticate_user(request.user.user_id, request.user.username, request.user.password)

        if not success or request.user.role not in (1, 3):
            return services_pb2.DeleteResultResponse(success=False, error_message=error_msg or 'User not authorized')

        if request.result.transaction_id != request.transaction.transaction_id or \
           request.result.transaction_id not in self.transactions:
            return services_pb2.DeleteResultResponse(success=False, error_message='Transaction mismatch or not found')

        rid = request.result.result_id
        if rid not in self.results:
            return services_pb2.DeleteResultResponse(success=False, error_message='Result not present')

        self.results.pop(rid)
        print(f'Deleted result with id = {rid}')
        return services_pb2.DeleteResultResponse(success=True, error_message='')

    def GetAllTransactions(self, request, context):
        """
        Returns all transactions to authorized users.

        Returns:
            GetAllTransactionsResponse: success status, error message, and list of transactions
        """
        self.log_info(request, context, "GetAllTransactions")
        auth_service = AuthenticationService()
        success, token, error_msg, role = auth_service.authenticate_user(request.user_id, request.username, request.password)

        if not success or request.role not in (1, 3):
            return services_pb2.GetAllTransactionsResponse(success=False, error_message=error_msg or 'User not authorized')

        all_transactions = [tx['transaction'] for tx in self.transactions.values()]
        return services_pb2.GetAllTransactionsResponse(user=request, success=True, error_message='', transactions=all_transactions)

    def FetchTransactionsOfUser(self, request, context):
        """
        Returns all transactions submitted by a user.

        Returns:
            FetchTransactionsOfUserResponse: success status, error message, and list of transactions
        """
        self.log_info(request, context, "FetchTransactionsOfUser")
        auth_service = AuthenticationService()
        success, token, error_msg, role = auth_service.authenticate_user(request.user_id, request.username, request.password)

        if not success or request.role not in (1, 3):
            return services_pb2.FetchTransactionsOfUserResponse(success=False, error_message=error_msg or 'User not authorized')

        user_transactions = [t['transaction'] for t in self.transactions.values() if t['transaction'].customer.user_id == request.user_id]
        return services_pb2.FetchTransactionsOfUserResponse(user=request, success=True, error_message='', transactions=user_transactions)

    def GetAllResults(self, request, context):
        """
        Returns all results in the system.

        Returns:
            GetAllResultsResponse: success status, error message, and list of results
        """
        self.log_info(request, context, "GetAllResults")
        auth_service = AuthenticationService()
        success, token, error_msg, role = auth_service.authenticate_user(request.user_id, request.username, request.password)

        if not success or request.role not in (1, 3):
            return services_pb2.GetAllResultsResponse(success=False, error_message=error_msg or 'User not authorized')

        all_results = [r['result'] for r in self.results.values()]
        return services_pb2.GetAllResultsResponse(user=request, success=True, error_message='', results=all_results)

    def FetchResultsOfTransaction(self, request, context):
        """
        Returns all results tied to a specific transaction.

        Returns:
            FetchResultsOfTransactionResponse: success status, error message, and list of results
        """
        self.log_info(request, context, "FetchResultIfTransaction")
        auth_service = AuthenticationService()
        success, token, error_msg, role = auth_service.authenticate_user(request.user.user_id, request.user.username, request.user.password)

        if not success or request.user.role not in (1, 3):
            return services_pb2.FetchResultOfTransactionResponse(success=False, error_message=error_msg or 'User not authorized')

        if request.transaction.transaction_id not in self.transactions:
            return services_pb2.FetchResultOfTransactionResponse(success=False, error_message='Transaction not present')

        related_results = [r['result'] for r in self.results.values() if r['result'].transaction_id == request.transaction.transaction_id]
        return services_pb2.FetchResultsOfTransactionResponse(success=True, error_message='', results=related_results)

def serve():
    """
    Starts the gRPC server and registers services.
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    services_pb2_grpc.add_AuthenticationServiceServicer_to_server(AuthenticationService(), server)
    services_pb2_grpc.add_TransactionServiceServicer_to_server(TransactionService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
