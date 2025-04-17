import grpc
import services_pb2
import services_pb2_grpc

if __name__ == '__main__':
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = services_pb2_grpc.AuthenticationServiceStub(channel)
        user0 = services_pb2.User(username = 'username1', password = 'password1')
        user1 = services_pb2.User(username = 'username2', password = 'password2')
        update_to_user = services_pb2.User(username = 'updated_username', password = 'updated_password')

        response_adduser1 = stub.AddUser(user0)
        print(f'First adduser request---\nExpected response = True\nActual response = {response_adduser1.success}\n')
        user0 = response_adduser1.users[0]

        response_adduser2 = stub.AddUser(user1) 
        print(f'Second adduser request---\nExpected response = True\nActual response = {response_adduser2.success}\n')
        user1 = response_adduser2.users[0]

        response_updateuser1 = stub.UpdateUser(services_pb2.UpdateUserMessage(
            old_user_data = user1, new_user_data = update_to_user))
        print(f'First updateuser request---\nExpected response = True\nActual response = {response_updateuser1.success}\n')

        response_deleteuser1 = stub.DeleteUser(user1)
        print(f'First deleteuser request---\nExpected response = True\nActual response = {response_deleteuser1.success}\n')



        response_false_1 = stub.Authenticate(services_pb2.AuthenticationMessage(
            username = '', password = '12345'))
        print(f'First authentication request---\nExpected response = False\nActual response = {response_false_1.success}\n')

        response_false_2 = stub.Authenticate(services_pb2.AuthenticationMessage(
            username = user0.username, password = 'notacorrectpassword'))
        print(f'Second authentication request---\nExpected response = False\nActual response = {response_false_2.success}\n')

        response_true = stub.Authenticate(services_pb2.AuthenticationMessage(
            username = user0.username, password = user0.password))
        print(f'Third authentication request---\nExpected response = True\nActual response = {response_true.success}\n')


        response_authorization_false = stub.VerifyToken(services_pb2.VerifyTokenMessage(
            user = user0, token = 'asdasd123'))
        print(f'First token validation request---\nExpected response = False\nActual response = {response_authorization_false.success}\n')

        response_authorization_true = stub.VerifyToken(services_pb2.VerifyTokenMessage(
            user = user0, token = response_true.token))
        print(f'Second token validation request---\nExpected response = True\nActual response = {response_authorization_true.success}\n')