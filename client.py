import grpc
import services_pb2
import services_pb2_grpc

def setup():
    # create user objects
    user1 = services_pb2.User(
        username='username1', 
        password='password1',
        role=services_pb2.Role.ADMINISTRATOR)
    user2 = services_pb2.User(username='username2', password='password2')
    user3 = services_pb2.User(username='username3', password='password3')

    # create transaction objects
    transaction1 = services_pb2.Transaction(
        transaction_id=0,
        customer=user1,
        status=services_pb2.Transaction.Status.submitted,
        amount=100
    )
    transaction2 = services_pb2.Transaction(
        transaction_id=0,
        customer=user2,
        status=services_pb2.Transaction.Status.submitted,
        amount=200
    )

    # create a dictionary to hold stuff
    objects = {
        'user1': user1,
        'user2': user2,
        'transaction1': transaction1,
        'transaction2': transaction2,
        'user3': user3,
    }
    return objects

def test_adding_user(objects):
    auth_stub = objects['auth_stub']

    # add user1
    response_adduser1 = auth_stub.AddUser(objects['user1'])
    objects['user1'] = response_adduser1.users[0] # update user1 with the response from the server (includes user_id)
    assert response_adduser1.success == True, f"response_adduser1: expected True, got {response_adduser1.success}" # assertion for success

    # add user2
    response_adduser2 = auth_stub.AddUser(objects['user2'])
    objects['user2'] = response_adduser2.users[0] # update user2 with the response from the server (includes user_id)
    assert response_adduser2.success == True, f"response_adduser2: expected True, got {response_adduser2.success}" # assertion for success

def test_updating_user(objects):
    auth_stub = objects['auth_stub']

    # update user1
    update_to_user = services_pb2.User(username='updated_username', password='updated_password', role=services_pb2.Role.ADMINISTRATOR)
    response_updateuser1 = auth_stub.UpdateUser(services_pb2.UpdateUserMessage(
        old_user_data=objects['user1'], new_user_data=update_to_user))
    assert response_updateuser1.success == True, f"response_updateuser1: expected True, got {response_updateuser1.success}" # assertion for success
    assert response_updateuser1.users[0].username == update_to_user.username, f"response_updateuser1: expected {update_to_user.username}, got {response_updateuser1.users[0].username}" # assertion for username
    assert response_updateuser1.users[0].password == update_to_user.password, f"response_updateuser1: expected {update_to_user.password}, got {response_updateuser1.users[0].password}" # assertion for password
    objects['user1'] = response_updateuser1.users[0] # update user1 with the response from the server (includes user_id)

def test_deleting_user(objects):
    auth_stub = objects['auth_stub']

    # delete user2
    response_deleteuser2 = auth_stub.DeleteUser(objects['user2'])
    assert response_deleteuser2.success == True, f"response_deleteuser2: expected True, got {response_deleteuser2.success}" # assertion for success

    # delete user3
    response_deleteuser3 = auth_stub.DeleteUser(objects['user3'])
    assert response_deleteuser3.success == False, f"response_deleteuser3: expected False, got {response_deleteuser3.success}" # assertion for failure

    # add user2 again
    response_adduser2 = auth_stub.AddUser(objects['user2'])
    objects['user2'] = response_adduser2.users[0] # update user2 with the response from the server (includes user_id)

def test_authenticating_user(objects):
    auth_stub = objects['auth_stub']

    # authenticate with actual credentials
    response_authenticate_true = auth_stub.Authenticate(services_pb2.AuthenticationMessage(
        user_id=objects['user1'].user_id, username=objects['user1'].username, password=objects['user1'].password))
    assert response_authenticate_true.success == True, f"response_authenticate_true: expected True, got {response_authenticate_true.success}" # assertion for success
    assert response_authenticate_true.role == objects['user1'].role, f"response_authenticate_true: expected {objects['user1'].role}, got {response_authenticate_true.role}" # assertion for role
    assert response_authenticate_true.token != '', f"response_authenticate_true: expected non-empty token, got {response_authenticate_true.token}" # assertion for token
    objects['response_authenticate_true'] = response_authenticate_true # store the response for later use

    # authenticate with empty credentials
    response_authenticate_empty = auth_stub.Authenticate(services_pb2.AuthenticationMessage(
        user_id=objects['user1'].user_id, username='', password=''))
    assert response_authenticate_empty.success == False, f"response_authenticate_false: expected False, got {response_authenticate_empty.success}" # assertion for failure
    
    # authenticate with incorrect credentials
    response_authenticate_false = auth_stub.Authenticate(services_pb2.AuthenticationMessage(
        user_id=objects['user1'].user_id, username=objects['user1'].username, password='notacorrectpassword'))
    assert response_authenticate_false.success == False, f"response_authenticate_false: expected False, got {response_authenticate_false.success}" # assertion for failure

def test_authorizing_user(objects):
    auth_stub = objects['auth_stub']

    # authorize user1 with correct token
    response_authorization_true = auth_stub.VerifyToken(services_pb2.VerifyTokenMessage(
        user=objects['user1'], token=objects['response_authenticate_true'].token))
    assert response_authorization_true.success == True, f"response_authorization_true: expected True, got {response_authorization_true.success}" # assertion for success

    # authorize user2 with incorrect token
    response_authorization_false = auth_stub.VerifyToken(services_pb2.VerifyTokenMessage(
        user=objects['user2'], token=objects['response_authenticate_true'].token))
    assert response_authorization_false.success == False, f"response_authorization_false: expected False, got {response_authorization_false.success}" # assertion for failure

def test_add_transaction(objects):
    transaction_stub = objects['transaction_stub']
    # add transaction1 after authorization
    response_addtransaction1 = transaction_stub.AddTransaction(services_pb2.AddTransactionMessage(
        user=objects['user1'], transaction=objects['transaction1']))
    assert response_addtransaction1.success == True, f"response_addtransaction1: expected True, got {response_addtransaction1.success}" # assertion for success
    objects['transaction1'] = response_addtransaction1.transactions[0] # update transaction1 with the response from the server (includes transaction_id)

    # add transaction2 with incorrect user
    response_addtransaction2 = transaction_stub.AddTransaction(services_pb2.AddTransactionMessage(
        user=objects['user3'], transaction=objects['transaction2']))
    assert response_addtransaction2.success == False, f"response_addtransaction2: expected False, got {response_addtransaction2.success}" # assertion for failure

def test_update_transaction(objects):
    transaction_stub = objects['transaction_stub']

    transcation_to_update = services_pb2.Transaction(
        transaction_id=objects['transaction1'].transaction_id,
        customer=objects['transaction1'].customer,
        status=services_pb2.Transaction.Status.accepted,
        amount=200
    )
    response_updatetransaction1 = transaction_stub.UpdateTransaction(services_pb2.UpdateTransactionMessage(
         user=objects['user1'], old_transaction_data=objects['transaction1'], new_transaction_data=transcation_to_update))
   
    if response_updatetransaction1.success == False:
        print(f"Error: {response_updatetransaction1.error_message}")

    assert response_updatetransaction1.success == True, f"response_updatetransaction1: expected True, got {response_updatetransaction1.success}" # assertion for success
    assert response_updatetransaction1.transactions[0].status == transcation_to_update.status, f"response_updatetransaction1: expected {transcation_to_update.status}, got {response_updatetransaction1.transactions[0].status}" # assertion for status
    objects['transaction1'] = response_updatetransaction1.transactions[0] # update transaction1 with the response from the server (includes transaction_id)

    # update transaction2 with incorrect user (since this user was never added, it will fail at the authentication step)
    response_updatetransaction2 = transaction_stub.UpdateTransaction(services_pb2.UpdateTransactionMessage(
        user=objects['user3'], old_transaction_data=objects['transaction1'], new_transaction_data=transcation_to_update))
    assert response_updatetransaction2.success == False, f"response_updatetransaction2: expected False, got {response_updatetransaction2.success}" # assertion for failure
    assert response_updatetransaction2.error_message == 'username or password is incorrect', f"response_updatetransaction2: expected 'username or password is incorrect', got {response_updatetransaction2.error_message}" # assertion for error message

def test_delete_transaction(objects):
    transaction_stub = objects['transaction_stub']

    # delete transaction1
    response_deletetransaction1 = transaction_stub.DeleteTransaction(services_pb2.DeleteTransactionMessage(
        user=objects['user1'], transaction=objects['transaction1']))
    if response_deletetransaction1.success == False:
        print(f"Error: {response_deletetransaction1.error_message}")
    assert response_deletetransaction1.success == True, f"response_deletetransaction1: expected True, got {response_deletetransaction1.success}" # assertion for success

    # delete transaction2 with incorrect user
    response_deletetransaction2 = transaction_stub.DeleteTransaction(services_pb2.DeleteTransactionMessage(
        user=objects['user3'], transaction=objects['transaction2']))
    assert response_deletetransaction2.success == False, f"response_deletetransaction2: expected False, got {response_deletetransaction2.success}" # assertion for failure

if __name__ == '__main__':
    # Establish a gRPC channel to the server running on localhost at port 50051
    with grpc.insecure_channel('localhost:50051') as channel:
        objects = setup()
        objects['auth_stub'] = services_pb2_grpc.AuthenticationServiceStub(channel) # Create a stub for the AuthenticationService
        objects['transaction_stub'] = services_pb2_grpc.TransactionServiceStub(channel) # Create a stub for the TransactionService

        test_adding_user(objects)
        test_updating_user(objects)
        test_deleting_user(objects)
        test_authenticating_user(objects)
        test_authorizing_user(objects) # works once only
        test_add_transaction(objects)
        test_update_transaction(objects)
        test_delete_transaction(objects)