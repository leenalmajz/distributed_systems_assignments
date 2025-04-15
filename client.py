import grpc
import services_pb2
import services_pb2_grpc

if __name__ == '__main__':
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = services_pb2_grpc.AuthenticationServiceStub(channel)
        user0 = services_pb2.User(username = 'username1', password = 'password1')

        response = stub.AddUser(user0)
        print(f'First request response = {response.success}')