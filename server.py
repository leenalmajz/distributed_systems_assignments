""" TODO:
    1. add documentation
    2. add context
    3. add testing"""

import grpc, secrets
from concurrent import futures
import logging
import services_pb2 
import services_pb2_grpc

class AuthenticationService(services_pb2_grpc.AuthenticationServiceServicer):
    users = {}
    current_id = 1

    def AddUser(self, request, context):
        """
        Implementation of the AddUser service method. Adds a user to the internal
        users list. If there is no id, the next highest id will be assigned to the new user.
        If there is a user with the same id, the request will be rejected.
        :param request: the request to process.
        :param context: grpc context object
        :return: an AddUserResponse object
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
        Implementation of the UpdateUser service method. Updates an already existing user in the internal
        users list. If there is no id (meaning the user doesn't exist), the function will return an error.
        :param request: the request to process.
        :param context: grpc context object
        :return: an UpdateUserResponse object
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
        Implementation of the DeleteUser service method. Deletes an existing user  from the internal
        users list. If there is no id (meaning the user doesn't exist), the function will return an error.
        :param request: the request to process.
        :param context: grpc context object
        :return: an DeleteUserResponse object
        """
        
        if request.user_id not in self.users:
            return services_pb2.DeleteUserResponse(success=False, error_message='User not present')
        
        user = self.users[request.user_id]['user']
        self.users.pop(request.user_id)
        print(f'Deleted user with id = {request.user_id} and name {user.username}')
        return services_pb2.DeleteUserResponse(success=True, error_message='')
    
    def Authenticate(self, request, context):
        """
        Implementation of the Authenticate service method. Checks whether a given username and password pair returns a user or not.
        :param request: the request to process.
        :param context: grpc context object
        :return: an AuthenticationResponse object
        """
        if request.username == "" or request.password == "":
            return services_pb2.AuthenticationResponse(success = False, error_message = 'username or password not given')
        
        for user_id, user_dict in self.users.items():
            if user_dict['user'].username == request.username and user_dict['user'].password == request.password:
                random_token = secrets.token_urlsafe(64)
                user_dict['token'] = random_token
                return services_pb2.AuthenticationResponse(success = True, error_message = '', role = user_dict['user'].role, token = random_token)
        return services_pb2.AuthenticationResponse(success = False, error_message = 'username or password is incorrect')

    def VerifyToken(self, request, context):
        """
        Implementation of the VerifyToken service method. Checks whether a given token for a given user is still valid or not.
        :param request: the request to process.
        :param context: grpc context object
        :return: a boolean
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
        Implementation of the AddTransaction service method.
        :param request:
        :param context:
        :return: an AddTransactionResponse object
        """

        if not AuthenticationService.Authenticate(services_pb2.AuthenticationMessage(request.user.username, request.user.password)).success:
            return services_pb2.AddTransactionResponse(success=False, error_message='User not authenticated')
        
        if request.user.role != 1 or request.user.role != 3:
            return services_pb2.AddTransactionResponse(success=False, error_message='User not authorized')
        
        if request.transaction.transaction_id == 0:
            request.transaction.transaction_id = self.current_transaction_id
            self.current_transaction_id += 1

        if request.transaction.transaction_id in self.transactions:
            return services_pb2.AddTransactionResponse(success=False, error_message='Transaction already present')

        self.transactions[request.transaction.transaction_id] = request.transaction
        print(f'Added new transaction with id = {request.transaction.transaction_id}')
        return services_pb2.AddTransactionResponse(success=True, error_message='', transactions=[request.transaction])
    
    def UpdateTransaction(self, request, context):
        """
        Implementation of the AddTransaction service method.
        :param request:
        :param context:
        :return: an UpdateTransactionResponse object.
        """

        if not AuthenticationService.Authenticate(services_pb2.AuthenticationMessage(request.user.username, request.user.password)).success:
            return services_pb2.UpdateTransactionResponse(success=False, error_message='User not authenticated')
        
        if request.user.role != 1 or request.user.role != 3:
            return services_pb2.UpdateTransactionResponse(success=False, error_message='User not authorized')
        
        if request.old_transaction_data.transaction_id not in self.transactions:
            return services_pb2.UpdateTransactionResponse(success=False, error_message='Transaction not present')
        
        id = request.old_transaction_data.transaction_id
        self.transactions[id].customer = request.new_transaction_data.customer
        self.transactions[id].status = request.new_transaction_data.status
        self.transactions[id].vendor_id = request.new_transaction_data.vendor_id
        self.transactions[id].amount = request.new_transaction_data.amount
        print(f'Updated transaction with id = {id}')
        return services_pb2.UpdateTransactionResponse(success=True, error_message='', transactions=[self.transactions[id]])
        
    def DeleteTransaction(self, request, cntext):
        """
        Implementation of the DeleteTransaction service method.
        :param request:
        :param context:
        :return: a DeleteTransactionResponse object.
        """

        if not AuthenticationService.Authenticate(services_pb2.AuthenticationMessage(request.user.username, request.user.password)).success:
            return services_pb2.DeleteTransactionResponse(success=False, error_message='User not authenticated')
        
        if request.user.role != 1 or request.user.role != 3:
            return services_pb2.DeleteTransactionResponse(success=False, error_message='User not authorized')
        
        if request.transaction.transaction_id not in self.transactions:
            return services_pb2.UpdateTransactionResponse(success=False, error_message='Transaction not present')
        
        transaction = self.transactions[request.transaction.transaction_id]
        self.transactions.pop(request.transaction.transaction_id)
        print(f'Deleted transaction with id = {request.transaction.transaction_id} and it\'s customer\'s name: {transaction.customer.username}')
        return services_pb2.DeleteTransactionResponse(success=True, error_message='')



    def AddResult(self, request, context):
        """
        Implementation of the AddResult service method.
        :param request:
        :param context:
        :return: an AddResultResponse object
        """

        if not AuthenticationService.Authenticate(services_pb2.AuthenticationMessage(request.user.username, request.user.password)).success:
            return services_pb2.AddResultResponse(success=False, error_message='User not authenticated')
        
        if request.user.role != 1 or request.user.role != 3:
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

        self.transactions[request.result.result_id] = request.result
        print(f'Added new result with id = {request.result.result_id}')
        return services_pb2.AddResultResponse(success=True, error_message='', results=[request.result])
    
    def UpdateResult(self, request, context):
        """
        Implementation of the UpdateResult service method.
        :param request:
        :param context:
        :return: an UpdateResultResponse object.
        """

        if not AuthenticationService.Authenticate(services_pb2.AuthenticationMessage(request.user.username, request.user.password)).success:
            return services_pb2.UpdateResultResponse(success=False, error_message='User not authenticated')
        
        if request.user.role != 1 or request.user.role != 3:
            return services_pb2.UpdateResultResponse(success=False, error_message='User not authorized')
        
        if request.new_result_data.transaction_id != request.transaction.transaction_id:
            return services_pb2.UpdateResultResponse(success=False, error_message='Transaction id mismatch')

        if request.new_result_data.transaction_id not in self.transactions:
            return services_pb2.UpdateResultResponse(success=False, error_message='Transaction not present')
        
        id = request.old_result_data.transaction_id
        self.results[id].transaction_id = request.new_result_data.transaction_id
        self.results[id].timestamp = request.new_result_data.timestamp
        self.results[id].is_fraudulent = request.new_result_data.is_fraudulent
        self.results[id].confidence = request.new_result_data.confidence
        print(f'Updated transaction with id = {id}')
        return services_pb2.UpdateResultResponse(success=True, error_message='', results=[self.results[id]])

    def DeleteResult(self, request, cntext):
        """
        Implementation of the DeleteResult service method.
        :param request:
        :param context:
        :return: a DeleteResultResponse object.
        """

        if not AuthenticationService.Authenticate(services_pb2.AuthenticationMessage(request.user.username, request.user.password)).success:
            return services_pb2.DeleteResultResponse(success=False, error_message='User not authenticated')
        
        if request.user.role != 1 or request.user.role != 3:
            return services_pb2.DeleteResultResponse(success=False, error_message='User not authorized')
        
        if request.result.transaction_id != request.transaction.transaction_id:
            return services_pb2.DeleteResultResponse(success=False, error_message='Transaction id mismatch')

        if request.result.transaction_id not in self.transactions:
            return services_pb2.DeleteResultResponse(success=False, error_message='Transaction not present')
        
        result = self.results[request.result.result_id]
        self.transactions.pop(request.result.result_id)
        print(f'Deleted transaction with id = {request.result.result_id} and it\'s transaction\'s id: {result.transaction_id}')
        return services_pb2.DeleteResultResponse(success=True, error_message='')
    


    def GetAllTransactions(self, request, context):
        """
        Implementation of the GetAllTransactions service method.
        :param request:
        :param context:
        :return: a table containing metadata information for each customer transaction (customer, timestamp, status (submitted, accepted, rejected), vendor-ID, amount).
        """

        if not AuthenticationService.Authenticate(services_pb2.AuthenticationMessage(request.username, request.password)).success:
            return services_pb2.GetAllTransactionsResponse(user=request, success=False, error_message='User not authenticated')
        
        if request.role != 1 or request.role != 3:
            return services_pb2.GetAllTransactionsResponse(user=request, success=False, error_message='User not authorized')
                
        return services_pb2.GetAllTransactionsResponse(user=request, success=True, error_message='', transactions=list(self.transactions.values()))
    
    def FetchTransactionsOfUser(self, request, context):
        """
        Implementation of the FetchTransactionsOfUser service method.
        :param request:
        :param context:
        :return: a table containing metadata information for each customer transaction (customer, timestamp, status (submitted, accepted, rejected), vendor-ID, amount).
        """

        if not AuthenticationService.Authenticate(services_pb2.AuthenticationMessage(request.username, request.password)).success:
            return services_pb2.FetchTransactionsOfUserResponse(user=request, success=False, error_message='User not authenticated')
        
        if request.role != 1 or request.role != 3:
            return services_pb2.FetchTransactionsOfUserResponse(user=request, success=False, error_message='User not authorized')
        
        found = []
        for transaction_id, transaction in self.transactions:
            if transaction.user_id == request.user_id:
                found.append(transaction)

        return services_pb2.FetchTransactionsOfUserResponse(user=request, success=True, error_message='', transactions=found)


 
    def GetAllResults(self, request, context):
        """
        Implementation of the GetAllResults service method.
        :param request:
        :param context:
        :return: a table containing metadata information for each customer transaction (customer, timestamp, status (submitted, accepted, rejected), vendor-ID, amount).
        """

        if not AuthenticationService.Authenticate(services_pb2.AuthenticationMessage(request.user.username, request.user.password)).success:
            return services_pb2.GetAllResultsResponse(user=request.user, result=request.result, success=False, error_message='User not authenticated')
        
        if request.user.role != 1 or request.user.role != 3:
            return services_pb2.GetAllResultsResponse(user=request.user, result=request.result, success=False, error_message='User not authorized')
        
        return services_pb2.GetAllResultsResponse(user=request.user, result=request.result, success=True, error_message='', results=list(self.results.values()))

    def FetchResultsOfTransaction(self, request, context):
        """
        Implementation of the FetchResultOfTransaction service method.
        :param request:
        :param context:
        :return: a table containing metadata information for each customer transaction (customer, timestamp, status (submitted, accepted, rejected), vendor-ID, amount).
        """
        
        if not AuthenticationService.Authenticate(services_pb2.AuthenticationMessage(request.user.username, request.user.password)).success:
            return services_pb2.FetchResultOfTransactionResponse(success=False, error_message='User not authenticated')
        
        if request.user.role != 1 or request.user.role != 3:
            return services_pb2.FetchResultOfTransactionResponse(success=False, error_message='User not authorized')
        
        if request.transaction.transaction_id not in self.transactions:
            return services_pb2.FetchResultOfTransactionResponse(success=False, error_message='Transaction not present')


        found = []
        for result_id, result in self.results.items():
            if result.transaction_id == request.transaction.transaction_id:
                found.append(result)
        
        return services_pb2.FetchResultsOfTransactionResponse(success=True, error_message='', results=[found])
    

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    services_pb2_grpc.add_AuthenticationServiceServicer_to_server(AuthenticationService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
