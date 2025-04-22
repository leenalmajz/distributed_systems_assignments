import grpc
import services_pb2
import services_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime, timezone

# Create a protobuf Timestamp from the current UTC time
now = datetime.now(timezone.utc)
proto_timestamp = Timestamp()
proto_timestamp.FromDatetime(now)

def setup():
    """
    Creates and returns a dictionary of test users and transactions for test cases.
    """
    # Define three test users
    user1 = services_pb2.User(
        username='username1', 
        password='password1',
        role=services_pb2.Role.ADMINISTRATOR
    )
    user2 = services_pb2.User(username='username2', password='password2')
    user3 = services_pb2.User(username='username3', password='password3')

    # Define two test transactions
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

    return {
        'user1': user1,
        'user2': user2,
        'transaction1': transaction1,
        'transaction2': transaction2,
        'user3': user3,
    }

def test_adding_user(objects):
    """
    Tests adding two users to the authentication service.
    """
    auth_stub = objects['auth_stub']

    # Add user1 and check response
    response_adduser1 = auth_stub.AddUser(objects['user1'])
    objects['user1'] = response_adduser1.users[0]
    assert response_adduser1.success == True

    # Add user2 and check response
    response_adduser2 = auth_stub.AddUser(objects['user2'])
    objects['user2'] = response_adduser2.users[0]
    assert response_adduser2.success == True

def test_updating_user(objects):
    """
    Tests updating a user's information.
    """
    auth_stub = objects['auth_stub']

    # Prepare updated user information
    update_to_user = services_pb2.User(
        username='updated_username',
        password='updated_password',
        role=services_pb2.Role.ADMINISTRATOR
    )

    # Attempt update
    response_updateuser1 = auth_stub.UpdateUser(services_pb2.UpdateUserMessage(
        old_user_data=objects['user1'], new_user_data=update_to_user))
    
    assert response_updateuser1.success == True
    assert response_updateuser1.users[0].username == update_to_user.username
    assert response_updateuser1.users[0].password == update_to_user.password
    objects['user1'] = response_updateuser1.users[0]

def test_deleting_user(objects):
    """
    Tests deleting users (including invalid user).
    """
    auth_stub = objects['auth_stub']

    # Delete user2
    response_deleteuser2 = auth_stub.DeleteUser(objects['user2'])
    assert response_deleteuser2.success == True

    # Try to delete user3 who was never added
    response_deleteuser3 = auth_stub.DeleteUser(objects['user3'])
    assert response_deleteuser3.success == False

    # Re-add user2 after deletion
    response_adduser2 = auth_stub.AddUser(objects['user2'])
    objects['user2'] = response_adduser2.users[0]

def test_authenticating_user(objects):
    """
    Tests user authentication with valid and invalid credentials.
    """
    auth_stub = objects['auth_stub']

    # Correct authentication
    response_authenticate_true = auth_stub.Authenticate(services_pb2.AuthenticationMessage(
        user_id=objects['user1'].user_id,
        username=objects['user1'].username,
        password=objects['user1'].password
    ))
    assert response_authenticate_true.success == True
    assert response_authenticate_true.role == objects['user1'].role
    assert response_authenticate_true.token != ''
    objects['response_authenticate_true'] = response_authenticate_true

    # Authentication with empty credentials
    response_authenticate_empty = auth_stub.Authenticate(services_pb2.AuthenticationMessage(
        user_id=objects['user1'].user_id, username='', password=''))
    assert response_authenticate_empty.success == False

    # Authentication with incorrect password
    response_authenticate_false = auth_stub.Authenticate(services_pb2.AuthenticationMessage(
        user_id=objects['user1'].user_id,
        username=objects['user1'].username,
        password='notacorrectpassword'
    ))
    assert response_authenticate_false.success == False

def test_authorizing_user(objects):
    """
    Tests token-based authorization for users.
    """
    auth_stub = objects['auth_stub']

    # Valid token for user1
    response_authorization_true = auth_stub.VerifyToken(services_pb2.VerifyTokenMessage(
        user=objects['user1'], token=objects['response_authenticate_true'].token))
    assert response_authorization_true.success == True

    # Token mismatch for user2
    response_authorization_false = auth_stub.VerifyToken(services_pb2.VerifyTokenMessage(
        user=objects['user2'], token=objects['response_authenticate_true'].token))
    assert response_authorization_false.success == False

def test_add_transaction(objects):
    """
    Tests adding transactions by authorized and unauthorized users.
    """
    transaction_stub = objects['transaction_stub']

    # Authorized transaction
    response_addtransaction1 = transaction_stub.AddTransaction(services_pb2.AddTransactionMessage(
        user=objects['user1'], transaction=objects['transaction1']))
    assert response_addtransaction1.success == True
    objects['transaction1'] = response_addtransaction1.transactions[0]

    # Unauthorized transaction by user3
    response_addtransaction2 = transaction_stub.AddTransaction(services_pb2.AddTransactionMessage(
        user=objects['user3'], transaction=objects['transaction2']))
    assert response_addtransaction2.success == False

def test_update_transaction(objects):
    """
    Tests updating a transaction with valid and invalid users.
    """
    transaction_stub = objects['transaction_stub']

    transcation_to_update = services_pb2.Transaction(
        transaction_id=objects['transaction1'].transaction_id,
        customer=objects['transaction1'].customer,
        status=services_pb2.Transaction.Status.accepted,
        amount=200
    )

    # Valid update by user1
    response_updatetransaction1 = transaction_stub.UpdateTransaction(services_pb2.UpdateTransactionMessage(
        user=objects['user1'],
        old_transaction_data=objects['transaction1'],
        new_transaction_data=transcation_to_update
    ))
    assert response_updatetransaction1.success == True
    assert response_updatetransaction1.transactions[0].status == transcation_to_update.status
    objects['transaction1'] = response_updatetransaction1.transactions[0]

    # Invalid update by user3
    response_updatetransaction2 = transaction_stub.UpdateTransaction(services_pb2.UpdateTransactionMessage(
        user=objects['user3'],
        old_transaction_data=objects['transaction1'],
        new_transaction_data=transcation_to_update
    ))
    assert response_updatetransaction2.success == False
    assert response_updatetransaction2.error_message == 'username or password is incorrect'

def test_delete_transaction(objects):
    """
    Tests deleting a transaction with valid and invalid users.
    """
    transaction_stub = objects['transaction_stub']

    # Re-add and then delete transaction2
    response_addtransaction2 = transaction_stub.AddTransaction(services_pb2.AddTransactionMessage(
        user=objects['user1'], transaction=objects['transaction2']))
    objects['transaction2'] = response_addtransaction2.transactions[0]

    response_deletetransaction1 = transaction_stub.DeleteTransaction(services_pb2.DeleteTransactionMessage(
        user=objects['user1'], transaction=objects['transaction2']))
    assert response_deletetransaction1.success == True

    # Invalid delete by user2
    response_deletetransaction2 = transaction_stub.DeleteTransaction(services_pb2.DeleteTransactionMessage(
        user=objects['user2'], transaction=objects['transaction1']))
    assert response_deletetransaction2.success == False

def test_add_result(objects):
    """
    Tests adding a result to a transaction.
    """
    transaction_stub = objects['transaction_stub']

    result = services_pb2.Result(
        result_id=0,
        transaction_id=objects['transaction1'].transaction_id,
        timestamp=proto_timestamp,
        is_fraudulent=False,
        confidence=0.85
    )

    response_addresult = transaction_stub.AddResult(services_pb2.AddResultMessage(
        user=objects['user1'], transaction=objects['transaction1'], result=result))
    assert response_addresult.success == True
    objects['result1'] = response_addresult.results[0]

def test_update_result(objects):
    """
    Tests updating an existing result.
    """
    transaction_stub = objects['transaction_stub']

    result_to_update = services_pb2.Result(
        result_id=objects['result1'].result_id,
        transaction_id=objects['transaction1'].transaction_id,
        timestamp=proto_timestamp,
        is_fraudulent=True,
        confidence=0.99
    )

    response_updateresult = transaction_stub.UpdateResult(services_pb2.UpdateResultMessage(
        user=objects['user1'], transaction=objects['transaction1'],
        old_result_data=objects['result1'], new_result_data=result_to_update
    ))
    assert response_updateresult.success == True
    assert response_updateresult.results[0].is_fraudulent == True
    objects['result1'] = response_updateresult.results[0]

def test_delete_result(objects):
    """
    Tests deleting a result from a transaction.
    """
    transaction_stub = objects['transaction_stub']

    response_deleteresult = transaction_stub.DeleteResult(services_pb2.DeleteResultMessage(
        user=objects['user1'], transaction=objects['transaction1'], result=objects['result1']))
    assert response_deleteresult.success == True

def test_get_all_transactions(objects):
    """
    Tests retrieving all transactions in the system.
    """
    transaction_stub = objects['transaction_stub']

    response_alltransactions = transaction_stub.GetAllTransactions(objects['user1'])
    assert response_alltransactions.success == True
    assert len(response_alltransactions.transactions) > 0
    assert response_alltransactions.transactions[0].transaction_id

def test_fetch_transactions_of_user(objects):
    """
    Tests fetching transactions created by a specific user.
    """
    transaction_stub = objects['transaction_stub']

    response_usertransactions = transaction_stub.FetchTransactionsOfUser(objects['user1'])
    assert response_usertransactions.success == True
    assert all(tx.customer.username == objects['user1'].username for tx in response_usertransactions.transactions)

def test_get_all_results(objects):
    """
    Tests retrieving all results in the system.
    """
    transaction_stub = objects['transaction_stub']

    # Ensure result exists first
    result = services_pb2.Result(
        result_id=0,
        transaction_id=objects['transaction1'].transaction_id,
        timestamp=proto_timestamp,
        is_fraudulent=False,
        confidence=0.75
    )
    response_addresult = transaction_stub.AddResult(services_pb2.AddResultMessage(
        user=objects['user1'], transaction=objects['transaction1'], result=result))
    assert response_addresult.success == True
    objects['result1'] = response_addresult.results[0]

    response_allresults = transaction_stub.GetAllResults(objects['user1'])
    assert response_allresults.success == True
    assert len(response_allresults.results) > 0
    assert response_allresults.results[0].result_id

def test_fetch_results_of_transaction(objects):
    """
    Tests fetching all results for a specific transaction.
    """
    transaction_stub = objects['transaction_stub']

    response_fetchresults = transaction_stub.FetchResultsOfTransaction(services_pb2.FetchResultsOfTransactionMessage(
        user=objects['user1'], transaction=objects['transaction1']
    ))
    assert response_fetchresults.success == True
    assert all(r.transaction_id == objects['transaction1'].transaction_id for r in response_fetchresults.results)

# Entry point for test execution
if __name__ == '__main__':
    # Setup channel and run all test cases
    with grpc.insecure_channel('localhost:50051') as channel:
        objects = setup()
        objects['auth_stub'] = services_pb2_grpc.AuthenticationServiceStub(channel)
        objects['transaction_stub'] = services_pb2_grpc.TransactionServiceStub(channel)

        # Sequentially run tests
        test_adding_user(objects)
        test_updating_user(objects)
        test_deleting_user(objects)
        test_authenticating_user(objects)
        test_authorizing_user(objects)
        test_add_transaction(objects)
        test_update_transaction(objects)
        test_delete_transaction(objects)
        test_add_result(objects)
        test_update_result(objects)
        test_delete_result(objects)
        test_get_all_transactions(objects)
        test_fetch_transactions_of_user(objects)
        test_get_all_results(objects)
        test_fetch_results_of_transaction(objects)