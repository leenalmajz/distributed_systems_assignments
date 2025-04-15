import grpc
from concurrent import futures
import logging
import services_pb2 
import services_pb2_grpc

class AuthenticationService(services_pb2_grpc.AuthenticationServiceServicer):
    users = {}
    users_id = 1

    def AddUser(self, request, context):
        """
        Implementation of the AddUser service method. Adds a user to the internal
        users list. If there is no id, the next highest id will be assigned to the new user.
        If there is a user with the same id, the request will be rejected.
        :param request: the request to process.
        :param context: grpc context object
        :return: an AddUserResponse object
        """
        if request.id == 0:
            request.id = self.current_id
            self.current_id += 1

        if request.id in self.users:
            return services_pb2_grpc.AddUserResponse(success=False, error_message='User already present')

        self.users[request.id] = {'user': request}
        print(f'Added new us with id = {request.user_id} and name {request.username}')
        return services_pb2.AddUserResponse(success=True, error_message='', users=[request])
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    services_pb2_grpc.add_AuthenticationServiceServicer_to_server(AuthenticationService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
