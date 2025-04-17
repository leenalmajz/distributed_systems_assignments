# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import services_pb2 as services__pb2

GRPC_GENERATED_VERSION = '1.71.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in services_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class AuthenticationServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.AddUser = channel.unary_unary(
                '/services.AuthenticationService/AddUser',
                request_serializer=services__pb2.User.SerializeToString,
                response_deserializer=services__pb2.AddUserResponse.FromString,
                _registered_method=True)
        self.UpdateUser = channel.unary_unary(
                '/services.AuthenticationService/UpdateUser',
                request_serializer=services__pb2.UpdateUserMessage.SerializeToString,
                response_deserializer=services__pb2.UpdateUserResponse.FromString,
                _registered_method=True)
        self.DeleteUser = channel.unary_unary(
                '/services.AuthenticationService/DeleteUser',
                request_serializer=services__pb2.User.SerializeToString,
                response_deserializer=services__pb2.DeleteUserResponse.FromString,
                _registered_method=True)
        self.Authenticate = channel.unary_unary(
                '/services.AuthenticationService/Authenticate',
                request_serializer=services__pb2.AuthenticationMessage.SerializeToString,
                response_deserializer=services__pb2.AuthenticationResponse.FromString,
                _registered_method=True)
        self.VerifyToken = channel.unary_unary(
                '/services.AuthenticationService/VerifyToken',
                request_serializer=services__pb2.VerifyTokenMessage.SerializeToString,
                response_deserializer=services__pb2.VerifyTokenResponse.FromString,
                _registered_method=True)


class AuthenticationServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def AddUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Authenticate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VerifyToken(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AuthenticationServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'AddUser': grpc.unary_unary_rpc_method_handler(
                    servicer.AddUser,
                    request_deserializer=services__pb2.User.FromString,
                    response_serializer=services__pb2.AddUserResponse.SerializeToString,
            ),
            'UpdateUser': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateUser,
                    request_deserializer=services__pb2.UpdateUserMessage.FromString,
                    response_serializer=services__pb2.UpdateUserResponse.SerializeToString,
            ),
            'DeleteUser': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteUser,
                    request_deserializer=services__pb2.User.FromString,
                    response_serializer=services__pb2.DeleteUserResponse.SerializeToString,
            ),
            'Authenticate': grpc.unary_unary_rpc_method_handler(
                    servicer.Authenticate,
                    request_deserializer=services__pb2.AuthenticationMessage.FromString,
                    response_serializer=services__pb2.AuthenticationResponse.SerializeToString,
            ),
            'VerifyToken': grpc.unary_unary_rpc_method_handler(
                    servicer.VerifyToken,
                    request_deserializer=services__pb2.VerifyTokenMessage.FromString,
                    response_serializer=services__pb2.VerifyTokenResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'services.AuthenticationService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('services.AuthenticationService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class AuthenticationService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def AddUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/services.AuthenticationService/AddUser',
            services__pb2.User.SerializeToString,
            services__pb2.AddUserResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UpdateUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/services.AuthenticationService/UpdateUser',
            services__pb2.UpdateUserMessage.SerializeToString,
            services__pb2.UpdateUserResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeleteUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/services.AuthenticationService/DeleteUser',
            services__pb2.User.SerializeToString,
            services__pb2.DeleteUserResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Authenticate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/services.AuthenticationService/Authenticate',
            services__pb2.AuthenticationMessage.SerializeToString,
            services__pb2.AuthenticationResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def VerifyToken(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/services.AuthenticationService/VerifyToken',
            services__pb2.VerifyTokenMessage.SerializeToString,
            services__pb2.VerifyTokenResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)


class TransactionServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.AddTransaction = channel.unary_unary(
                '/services.TransactionService/AddTransaction',
                request_serializer=services__pb2.AddTransactionMessage.SerializeToString,
                response_deserializer=services__pb2.AddTransactionResponse.FromString,
                _registered_method=True)
        self.UpdateTransaction = channel.unary_unary(
                '/services.TransactionService/UpdateTransaction',
                request_serializer=services__pb2.UpdateTransactionMessage.SerializeToString,
                response_deserializer=services__pb2.UpdateTransactionResponse.FromString,
                _registered_method=True)
        self.DeleteTransaction = channel.unary_unary(
                '/services.TransactionService/DeleteTransaction',
                request_serializer=services__pb2.DeleteTransactionMessage.SerializeToString,
                response_deserializer=services__pb2.DeleteTransactionResponse.FromString,
                _registered_method=True)
        self.AddResult = channel.unary_unary(
                '/services.TransactionService/AddResult',
                request_serializer=services__pb2.AddResultMessage.SerializeToString,
                response_deserializer=services__pb2.AddResultResponse.FromString,
                _registered_method=True)
        self.UpdateResult = channel.unary_unary(
                '/services.TransactionService/UpdateResult',
                request_serializer=services__pb2.UpdateResultMessage.SerializeToString,
                response_deserializer=services__pb2.UpdateResultResponse.FromString,
                _registered_method=True)
        self.DeleteResult = channel.unary_unary(
                '/services.TransactionService/DeleteResult',
                request_serializer=services__pb2.DeleteResultMessage.SerializeToString,
                response_deserializer=services__pb2.DeleteResultResponse.FromString,
                _registered_method=True)
        self.GetAllTransactions = channel.unary_unary(
                '/services.TransactionService/GetAllTransactions',
                request_serializer=services__pb2.User.SerializeToString,
                response_deserializer=services__pb2.GetAllTransactionsResponse.FromString,
                _registered_method=True)
        self.FetchTransactionsOfUser = channel.unary_unary(
                '/services.TransactionService/FetchTransactionsOfUser',
                request_serializer=services__pb2.User.SerializeToString,
                response_deserializer=services__pb2.FetchTransactionsOfUserResponse.FromString,
                _registered_method=True)
        self.GetAllResults = channel.unary_unary(
                '/services.TransactionService/GetAllResults',
                request_serializer=services__pb2.User.SerializeToString,
                response_deserializer=services__pb2.GetAllResultsResponse.FromString,
                _registered_method=True)
        self.FetchResultsOfTransaction = channel.unary_unary(
                '/services.TransactionService/FetchResultsOfTransaction',
                request_serializer=services__pb2.FetchResultsOfTransactionMessage.SerializeToString,
                response_deserializer=services__pb2.FetchResultsOfTransactionResponse.FromString,
                _registered_method=True)


class TransactionServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def AddTransaction(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateTransaction(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteTransaction(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddResult(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateResult(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteResult(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllTransactions(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FetchTransactionsOfUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllResults(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FetchResultsOfTransaction(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TransactionServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'AddTransaction': grpc.unary_unary_rpc_method_handler(
                    servicer.AddTransaction,
                    request_deserializer=services__pb2.AddTransactionMessage.FromString,
                    response_serializer=services__pb2.AddTransactionResponse.SerializeToString,
            ),
            'UpdateTransaction': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateTransaction,
                    request_deserializer=services__pb2.UpdateTransactionMessage.FromString,
                    response_serializer=services__pb2.UpdateTransactionResponse.SerializeToString,
            ),
            'DeleteTransaction': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteTransaction,
                    request_deserializer=services__pb2.DeleteTransactionMessage.FromString,
                    response_serializer=services__pb2.DeleteTransactionResponse.SerializeToString,
            ),
            'AddResult': grpc.unary_unary_rpc_method_handler(
                    servicer.AddResult,
                    request_deserializer=services__pb2.AddResultMessage.FromString,
                    response_serializer=services__pb2.AddResultResponse.SerializeToString,
            ),
            'UpdateResult': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateResult,
                    request_deserializer=services__pb2.UpdateResultMessage.FromString,
                    response_serializer=services__pb2.UpdateResultResponse.SerializeToString,
            ),
            'DeleteResult': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteResult,
                    request_deserializer=services__pb2.DeleteResultMessage.FromString,
                    response_serializer=services__pb2.DeleteResultResponse.SerializeToString,
            ),
            'GetAllTransactions': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllTransactions,
                    request_deserializer=services__pb2.User.FromString,
                    response_serializer=services__pb2.GetAllTransactionsResponse.SerializeToString,
            ),
            'FetchTransactionsOfUser': grpc.unary_unary_rpc_method_handler(
                    servicer.FetchTransactionsOfUser,
                    request_deserializer=services__pb2.User.FromString,
                    response_serializer=services__pb2.FetchTransactionsOfUserResponse.SerializeToString,
            ),
            'GetAllResults': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllResults,
                    request_deserializer=services__pb2.User.FromString,
                    response_serializer=services__pb2.GetAllResultsResponse.SerializeToString,
            ),
            'FetchResultsOfTransaction': grpc.unary_unary_rpc_method_handler(
                    servicer.FetchResultsOfTransaction,
                    request_deserializer=services__pb2.FetchResultsOfTransactionMessage.FromString,
                    response_serializer=services__pb2.FetchResultsOfTransactionResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'services.TransactionService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('services.TransactionService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class TransactionService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def AddTransaction(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/services.TransactionService/AddTransaction',
            services__pb2.AddTransactionMessage.SerializeToString,
            services__pb2.AddTransactionResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UpdateTransaction(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/services.TransactionService/UpdateTransaction',
            services__pb2.UpdateTransactionMessage.SerializeToString,
            services__pb2.UpdateTransactionResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeleteTransaction(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/services.TransactionService/DeleteTransaction',
            services__pb2.DeleteTransactionMessage.SerializeToString,
            services__pb2.DeleteTransactionResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def AddResult(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/services.TransactionService/AddResult',
            services__pb2.AddResultMessage.SerializeToString,
            services__pb2.AddResultResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UpdateResult(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/services.TransactionService/UpdateResult',
            services__pb2.UpdateResultMessage.SerializeToString,
            services__pb2.UpdateResultResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeleteResult(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/services.TransactionService/DeleteResult',
            services__pb2.DeleteResultMessage.SerializeToString,
            services__pb2.DeleteResultResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetAllTransactions(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/services.TransactionService/GetAllTransactions',
            services__pb2.User.SerializeToString,
            services__pb2.GetAllTransactionsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def FetchTransactionsOfUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/services.TransactionService/FetchTransactionsOfUser',
            services__pb2.User.SerializeToString,
            services__pb2.FetchTransactionsOfUserResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetAllResults(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/services.TransactionService/GetAllResults',
            services__pb2.User.SerializeToString,
            services__pb2.GetAllResultsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def FetchResultsOfTransaction(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/services.TransactionService/FetchResultsOfTransaction',
            services__pb2.FetchResultsOfTransactionMessage.SerializeToString,
            services__pb2.FetchResultsOfTransactionResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
