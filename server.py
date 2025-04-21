""" TODO:
    1. add documentation
    2. add context
    3. add testing"""

import grpc, secrets, logging
from concurrent import futures
import services_pb2 
import services_pb2_grpc

class AuthenticationService(services_pb2_grpc.AuthenticationServiceServicer):
    users = {}
    current_id = 1

    def authenticate_user(self, user_id, username, password):
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
        Adds a new user to the server's in-memory database.
        Automatically assigns a unique user ID and generates a token.
        
        Returns:
            AddUserResponse with the created user and success status.
        """
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
        Updates the details (username, password, role) of an existing user.
        
        Returns:
            UpdateUserResponse with the updated user and success status.
        """
        
        if request.old_user_data.user_id not in self.users:
            return services_pb2.UpdateUserResponse(success=False, error_message='User not present')
        self.users[request.old_user_data.user_id]['user'].username = request.new_user_data.username
        self.users[request.old_user_data.user_id]['user'].password = request.new_user_data.password
        self.users[request.old_user_data.user_id]['user'].role = request.new_user_data.role

        print(f'Updated user with id = {request.old_user_data.user_id} and name {request.new_user_data.username}')
        return services_pb2.UpdateUserResponse(success=True, error_message='', users=[self.users[request.old_user_data.user_id]['user']])

    def DeleteUser(self, request, context):
        """
        Deletes an existing user from the server.
        
        Returns:
            DeleteUserResponse indicating success or failure.
        """
        
        if request.user_id not in self.users:
            return services_pb2.DeleteUserResponse(success=False, error_message='User not present')
        
        user = self.users[request.user_id]['user']
        self.users.pop(request.user_id)
        print(f'Deleted user with id = {request.user_id} and name {user.username}')
        return services_pb2.DeleteUserResponse(success=True, error_message='')
    
    def Authenticate(self, request, context):
        """
        Authenticates a user based on their username and password.
        Generates and returns a new token if authentication succeeds.
        
        Returns:
            AuthenticationResponse with token, role, and status.
        """
        success, token, error_msg, role = self.authenticate_user(request.user_id, request.username, request.password)
        if success:
            return services_pb2.AuthenticationResponse(success=True, error_message='', role=role, token=token)
        else:
            return services_pb2.AuthenticationResponse(success=False, error_message=error_msg)

    def VerifyToken(self, request, context):
        """
        Verifies if the provided token matches the stored token for the given user.
        
        Returns:
            VerifyTokenResponse indicating whether the token is valid.
        """
        if request.token == '':
            return services_pb2.VerifyTokenResponse(success = False)
        
        if request.user.user_id not in self.users:
            return services_pb2.VerifyTokenResponse(success = False)
        
        user_dict = self.users[request.user.user_id]


        if user_dict['user'] == request.user and user_dict['token'] == request.token:
            return services_pb2.VerifyTokenResponse(success = True)
        return services_pb2.VerifyTokenResponse(success = False)


class TransactionService(services_pb2_grpc.TransactionServiceServicer):
    transactions = {} # stores transactions ids as keys and transaction objects as value
    results = {} # stores result ids as keys and result objects as values
    current_transaction_id = 1
    current_result_id = 1

    def AddTransaction(self, request, context):
        """
        Adds a new transaction to the server if the user is authenticated and authorized.
        Assigns a unique transaction ID.

        Returns:
            AddTransactionResponse with the created transaction and success status.
        """

        auth_service = AuthenticationService()
        success, token, error_msg, role = auth_service.authenticate_user(request.user.user_id, request.user.username, request.user.password)

        if not success:
            return services_pb2.AddTransactionResponse(success=False, error_message=error_msg)
        
        if request.user.role != 1 and request.user.role != 3:
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
        Updates an existing transaction's customer, status, vendor_id, and amount.
        Requires valid authentication and authorization.

        Returns:
            UpdateTransactionResponse with updated transaction and status.
        """

        auth_service = AuthenticationService()
        success, token, error_msg, role = auth_service.authenticate_user(request.user.user_id, request.user.username, request.user.password)

        if not success:
            return services_pb2.UpdateTransactionResponse(success=False, error_message=error_msg)
        
        if request.user.role != 1 and request.user.role != 3:
            return services_pb2.UpdateTransactionResponse(success=False, error_message='User not authorized')
        
        if request.old_transaction_data.transaction_id not in self.transactions:
            return services_pb2.UpdateTransactionResponse(success=False, error_message='Transaction not present')
        
        id = request.old_transaction_data.transaction_id
        transaction = self.transactions[id]['transaction']
        transaction.customer.CopyFrom(request.new_transaction_data.customer)
        transaction.status = request.new_transaction_data.status
        transaction.vendor_id = request.new_transaction_data.vendor_id
        transaction.amount = request.new_transaction_data.amount

        print(f'Updated transaction with id = {id}')
        return services_pb2.UpdateTransactionResponse(success=True, error_message='', transactions=[transaction])
        
    def DeleteTransaction(self, request, context):
        """
        Deletes an existing transaction.
        Only authorized users can delete transactions.

        Returns:
            DeleteTransactionResponse indicating success or failure.
        """

        auth_service = AuthenticationService()
        success, token, error_msg, role = auth_service.authenticate_user(request.user.user_id, request.user.username, request.user.password)

        if not success:
            return services_pb2.DeleteTransactionResponse(success=False, error_message=error_msg)
        
        if request.user.role != 1 and request.user.role != 3:
            return services_pb2.DeleteTransactionResponse(success=False, error_message='User not authorized')
        
        if request.transaction.transaction_id not in self.transactions:
            return services_pb2.DeleteTransactionResponse(success=False, error_message='Transaction not present')
        
        transaction = self.transactions[request.transaction.transaction_id]['transaction']
        self.transactions.pop(request.transaction.transaction_id)
        print(f'Deleted transaction with id = {request.transaction.transaction_id} and it\'s customer\'s name: {transaction.customer.username}')
        return services_pb2.DeleteTransactionResponse(success=True, error_message='')



    def AddResult(self, request, context):
        """
        Adds a new result tied to an existing transaction.
        Ensures the transaction exists and the result ID is unique.

        Returns:
            AddResultResponse with the created result and success status.
        """

        auth_service = AuthenticationService()
        success, token, error_msg, role = auth_service.authenticate_user(request.user.user_id, request.user.username, request.user.password)

        if not success:
            return services_pb2.AddResultResponse(success=False, error_message=error_msg)
        
        if request.user.role != 1 and request.user.role != 3:
            return services_pb2.AddResultResponse(success=False, error_message='User not authorized')
        
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
        Updates a result's data including timestamp, fraud status, and confidence score.
        User must be authorized, and the result must already exist.

        Returns:
            UpdateResultResponse with the updated result and status.
        """

        auth_service = AuthenticationService()
        success, token, error_msg, role = auth_service.authenticate_user(request.user.user_id, request.user.username, request.user.password)

        if not success:
            return services_pb2.UpdateResultResponse(success=False, error_message=error_msg)
        
        if request.user.role != 1 and request.user.role != 3:
            return services_pb2.UpdateResultResponse(success=False, error_message='User not authorized')
        
        if request.new_result_data.transaction_id != request.transaction.transaction_id:
            return services_pb2.UpdateResultResponse(success=False, error_message='Transaction id mismatch')

        if request.new_result_data.transaction_id not in self.transactions:
            return services_pb2.UpdateResultResponse(success=False, error_message='Transaction not present')
        
        if request.old_result_data.result_id not in self.results:
            return services_pb2.UpdateResultResponse(success=False, error_message='Result not present')
        
        id = request.old_result_data.result_id
        result = self.results[id]['result']
        result.transaction_id = request.new_result_data.transaction_id
        result.timestamp.CopyFrom(request.new_result_data.timestamp)
        result.is_fraudulent = request.new_result_data.is_fraudulent
        result.confidence = request.new_result_data.confidence
        print(f'Updated transaction with id = {id}')
        return services_pb2.UpdateResultResponse(success=True, error_message='', results=[result])

    def DeleteResult(self, request, cntext):
        """
        Deletes a result based on its ID and associated transaction.
        Ensures authorization and transaction validity.

        Returns:
            DeleteResultResponse indicating success or failure.
        """

        auth_service = AuthenticationService()
        success, token, error_msg, role = auth_service.authenticate_user(request.user.user_id, request.user.username, request.user.password)

        if not success:
            return services_pb2.DeleteResultResponse(success=False, error_message=error_msg)
        
        if request.user.role != 1 and request.user.role != 3:
            return services_pb2.DeleteResultResponse(success=False, error_message='User not authorized')
        
        if request.result.transaction_id != request.transaction.transaction_id:
            return services_pb2.DeleteResultResponse(success=False, error_message='Transaction id mismatch')

        if request.result.transaction_id not in self.transactions:
            return services_pb2.DeleteResultResponse(success=False, error_message='Transaction not present')
        
        if request.result.result_id not in self.results:
            return services_pb2.UpdateResultResponse(success=False, error_message='Result not present')
        
        result = self.results[request.result.result_id]['result']
        self.results.pop(request.result.result_id)
        print(f'Deleted transaction with id = {request.result.result_id} and it\'s transaction\'s id: {result.transaction_id}')
        return services_pb2.DeleteResultResponse(success=True, error_message='')
    


    def GetAllTransactions(self, request, context):
        """
        Retrieves all transactions stored on the server.
        Only users with the appropriate role may access this data.

        Returns:
            GetAllTransactionsResponse with a list of transactions.
        """

        auth_service = AuthenticationService()
        success, token, error_msg, role = auth_service.authenticate_user(request.user_id, request.username, request.password)

        if not success:
            return services_pb2.GetAllTransactionsResponse(success=False, error_message=error_msg)
        
        if request.role != 1 and request.role != 3:
            return services_pb2.GetAllTransactionsResponse(user=request, success=False, error_message='User not authorized')
        
        found = []
        for t_dict in self.transactions.values():
            found.append(t_dict['transaction'])

        return services_pb2.GetAllTransactionsResponse(user=request, success=True, error_message='', transactions=found)
    
    def FetchTransactionsOfUser(self, request, context):
        """
        Retrieves all transactions submitted by a specific user.
        Requires authentication and authorization.

        Returns:
            FetchTransactionsOfUserResponse with the user's transactions.
        """

        auth_service = AuthenticationService()
        success, token, error_msg, role = auth_service.authenticate_user(request.user_id, request.username, request.password)

        if not success:
            return services_pb2.FetchTransactionsOfUserResponse(success=False, error_message=error_msg)
        
        if request.role != 1 and request.role != 3:
            return services_pb2.FetchTransactionsOfUserResponse(user=request, success=False, error_message='User not authorized')
        
        found = []
        for transaction_id, transaction_dict in self.transactions.items():
            if transaction_dict['transaction'].customer.user_id == request.user_id:
                found.append(transaction_dict['transaction'])

        return services_pb2.FetchTransactionsOfUserResponse(user=request, success=True, error_message='', transactions=found)


 
    def GetAllResults(self, request, context):
        """
        Retrieves all results from the server.
        Requires user authentication and authorization.

        Returns:
            GetAllResultsResponse with a list of all results.
        """

        auth_service = AuthenticationService()
        success, token, error_msg, role = auth_service.authenticate_user(request.user_id, request.username, request.password)

        if not success:
            return services_pb2.GetAllResultsResponse(success=False, error_message=error_msg)
        
        if request.role != 1 and request.role != 3:
            return services_pb2.GetAllResultsResponse(user=request, success=False, error_message='User not authorized')
        
        found = []
        for r_dict in self.results.values():
            found.append(r_dict['result'])

        return services_pb2.GetAllResultsResponse(user=request, success=True, error_message='', results=found)

    def FetchResultsOfTransaction(self, request, context):
        """
        Fetches all results associated with a specific transaction.
        Requires the user to be authenticated and authorized.

        Returns:
            FetchResultsOfTransactionResponse with results tied to the transaction.
        """
        
        auth_service = AuthenticationService()
        success, token, error_msg, role = auth_service.authenticate_user(request.user.user_id, request.user.username, request.user.password)

        if not success:
            return services_pb2.FetchResultOfTransactionResponse(success=False, error_message=error_msg)
        
        if request.user.role != 1 and request.user.role != 3:
            return services_pb2.FetchResultOfTransactionResponse(success=False, error_message='User not authorized')
        
        if request.transaction.transaction_id not in self.transactions:
            return services_pb2.FetchResultOfTransactionResponse(success=False, error_message='Transaction not present')


        found = []
        for result_id, result_dict in self.results.items():
            if result_dict['result'].transaction_id == request.transaction.transaction_id:
                found.append(result_dict['result'])
        
        return services_pb2.FetchResultsOfTransactionResponse(success=True, error_message='', results=found)
    

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
