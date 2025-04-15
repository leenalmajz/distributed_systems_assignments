import grpc
import services_pb2
import services_pb2_grpc

if __name__ == '__main__':
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = services_pb2_grpc.AuthenticationServiceStub(channel)
        user0 = services_pb2.User(username = 'username1', password = 'password1')
        user1 = services_pb2.User(username = 'username2', password = 'password2')

        response_adduser1 = stub.AddUser(user0)
        print(f'First adduser request response = {response_adduser1.success}')

        response_adduser2 = stub.AddUser(user1) 
        print(f'Second adduser request response = {response_adduser2.success}')

        response_updateuser1 = stub.UpdateUser(services_pb2.UpdateUserMessage(user1, services_pb2.User(username = 'updated_username', password = 'updated_password')))
        print(f'First updateuser request response = {response_updateuser1.success}')

        response_deleteuser1 = stub.DeleteUser(user1)
        print(f'First deleteuser request response = {response_deleteuser1.success}')



        response_false_1 = stub.Authenticate(services_pb2.AuthenticationMessage('', '12345'))
        print(f'First authentication request response = {response_false_1.success}')

        response_false_2 = stub.Authenticate(services_pb2.AuthenticationMessage(user0.username, 'notacorrectpassword'))
        print(f'Second authentication request response = {response_false_2.success}')

        response_true = stub.Authenticate(services_pb2.AuthenticationMessage(user0.username, user0.password))
        print(f'Third authentication request response = {response_true.success}')