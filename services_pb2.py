# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: services.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'services.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0eservices.proto\x12\x08services\x1a\x1fgoogle/protobuf/timestamp.proto\"Y\n\x04User\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x10\n\x08password\x18\x03 \x01(\t\x12\x1c\n\x04role\x18\x04 \x01(\x0e\x32\x0e.services.Role\"X\n\x0f\x41\x64\x64UserResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x15\n\rerror_message\x18\x02 \x01(\t\x12\x1d\n\x05users\x18\x03 \x03(\x0b\x32\x0e.services.User\"a\n\x11UpdateUserMessage\x12%\n\rold_user_data\x18\x01 \x01(\x0b\x32\x0e.services.User\x12%\n\rnew_user_data\x18\x02 \x01(\x0b\x32\x0e.services.User\"[\n\x12UpdateUserResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x15\n\rerror_message\x18\x02 \x01(\t\x12\x1d\n\x05users\x18\x03 \x03(\x0b\x32\x0e.services.User\"<\n\x12\x44\x65leteUserResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x15\n\rerror_message\x18\x02 \x01(\t\";\n\x15\x41uthenticationMessage\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"m\n\x16\x41uthenticationResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x15\n\rerror_message\x18\x02 \x01(\t\x12\x1c\n\x04role\x18\x03 \x01(\x0e\x32\x0e.services.Role\x12\r\n\x05token\x18\x04 \x01(\t\"A\n\x12VerifyTokenMessage\x12\x1c\n\x04user\x18\x01 \x01(\x0b\x32\x0e.services.User\x12\r\n\x05token\x18\x02 \x01(\t\"&\n\x13VerifyTokenResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\xcd\x01\n\x0bTransaction\x12\x16\n\x0etransaction_id\x18\x01 \x01(\x05\x12 \n\x08\x63ustomer\x18\x02 \x01(\x0b\x32\x0e.services.User\x12,\n\x06status\x18\x03 \x01(\x0e\x32\x1c.services.Transaction.Status\x12\x11\n\tvendor_id\x18\x04 \x01(\x05\x12\x0e\n\x06\x61mount\x18\x05 \x01(\x05\"3\n\x06Status\x12\r\n\tsubmitted\x10\x00\x12\x0c\n\x08\x61\x63\x63\x65pted\x10\x01\x12\x0c\n\x08rejected\x10\x02\"a\n\x15\x41\x64\x64TransactionMessage\x12\x1c\n\x04user\x18\x01 \x01(\x0b\x32\x0e.services.User\x12*\n\x0bTransaction\x18\x02 \x01(\x0b\x32\x15.services.Transaction\"m\n\x16\x41\x64\x64TransactionResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x15\n\rerror_message\x18\x02 \x01(\t\x12+\n\x0ctransactions\x18\x03 \x03(\x0b\x32\x15.services.Transaction\"\xa2\x01\n\x18UpdateTransactionMessage\x12\x1c\n\x04user\x18\x01 \x01(\x0b\x32\x0e.services.User\x12\x33\n\x14old_transaction_data\x18\x02 \x01(\x0b\x32\x15.services.Transaction\x12\x33\n\x14new_transaction_data\x18\x03 \x01(\x0b\x32\x15.services.Transaction\"\x8e\x01\n\x19UpdateTransactionResponse\x12\x1c\n\x04user\x18\x01 \x01(\x0b\x32\x0e.services.User\x12\x0f\n\x07success\x18\x02 \x01(\x08\x12\x15\n\rerror_message\x18\x03 \x01(\t\x12+\n\x0ctransactions\x18\x04 \x03(\x0b\x32\x15.services.Transaction\"d\n\x18\x44\x65leteTransactionMessage\x12\x1c\n\x04user\x18\x01 \x01(\x0b\x32\x0e.services.User\x12*\n\x0btransaction\x18\x02 \x01(\x0b\x32\x15.services.Transaction\"C\n\x19\x44\x65leteTransactionResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x15\n\rerror_message\x18\x02 \x01(\t\"\x8d\x01\n\x06Result\x12\x11\n\tResult_id\x18\x01 \x01(\x05\x12\x16\n\x0etransaction_id\x18\x02 \x01(\x05\x12-\n\ttimestamp\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x15\n\ris_fraudulent\x18\x04 \x01(\x08\x12\x12\n\nconfidence\x18\x05 \x01(\x05\"~\n\x10\x41\x64\x64ResultMessage\x12\x1c\n\x04user\x18\x01 \x01(\x0b\x32\x0e.services.User\x12*\n\x0bTransaction\x18\x02 \x01(\x0b\x32\x15.services.Transaction\x12 \n\x06result\x18\x03 \x01(\x0b\x32\x10.services.Result\"^\n\x11\x41\x64\x64ResultResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x15\n\rerror_message\x18\x02 \x01(\t\x12!\n\x07results\x18\x03 \x03(\x0b\x32\x10.services.Result\"\xb5\x01\n\x13UpdateResultMessage\x12\x1c\n\x04user\x18\x01 \x01(\x0b\x32\x0e.services.User\x12*\n\x0btransaction\x18\x02 \x01(\x0b\x32\x15.services.Transaction\x12)\n\x0fold_result_data\x18\x03 \x01(\x0b\x32\x10.services.Result\x12)\n\x0fnew_result_data\x18\x04 \x01(\x0b\x32\x10.services.Result\"\x7f\n\x14UpdateResultResponse\x12\x1c\n\x04user\x18\x01 \x01(\x0b\x32\x0e.services.User\x12\x0f\n\x07success\x18\x02 \x01(\x08\x12\x15\n\rerror_message\x18\x03 \x01(\t\x12!\n\x07results\x18\x04 \x03(\x0b\x32\x10.services.Result\"\x81\x01\n\x13\x44\x65leteResultMessage\x12\x1c\n\x04user\x18\x01 \x01(\x0b\x32\x0e.services.User\x12*\n\x0btransaction\x18\x02 \x01(\x0b\x32\x15.services.Transaction\x12 \n\x06result\x18\x03 \x01(\x0b\x32\x10.services.Result\">\n\x14\x44\x65leteResultResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x15\n\rerror_message\x18\x02 \x01(\t\"\x94\x01\n\x1f\x46\x65tchTransactionsOfUserResponse\x12\x1c\n\x04user\x18\x01 \x01(\x0b\x32\x0e.services.User\x12\x0f\n\x07success\x18\x02 \x01(\x08\x12\x15\n\rerror_message\x18\x03 \x01(\t\x12+\n\x0ctransactions\x18\x04 \x03(\x0b\x32\x15.services.Transaction\"\x8f\x01\n\x1aGetAllTransactionsResponse\x12\x1c\n\x04user\x18\x01 \x01(\x0b\x32\x0e.services.User\x12\x0f\n\x07success\x18\x02 \x01(\x08\x12\x15\n\rerror_message\x18\x03 \x01(\t\x12+\n\x0ctransactions\x18\x04 \x03(\x0b\x32\x15.services.Transaction\"l\n FetchResultsOfTransactionMessage\x12\x1c\n\x04user\x18\x01 \x01(\x0b\x32\x0e.services.User\x12*\n\x0btransaction\x18\x02 \x01(\x0b\x32\x15.services.Transaction\"m\n!FetchResultsOfTransactionResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x15\n\rerror_message\x18\x02 \x01(\t\x12 \n\x06Result\x18\x03 \x03(\x0b\x32\x10.services.Result\"4\n\x14GetAllResultsMessage\x12\x1c\n\x04user\x18\x01 \x01(\x0b\x32\x0e.services.User\"\x80\x01\n\x15GetAllResultsResponse\x12\x1c\n\x04user\x18\x01 \x01(\x0b\x32\x0e.services.User\x12\x0f\n\x07success\x18\x02 \x01(\x08\x12\x15\n\rerror_message\x18\x03 \x01(\t\x12!\n\x07Results\x18\x04 \x03(\x0b\x32\x10.services.Result*>\n\x04Role\x12\t\n\x05\x42\x41SIC\x10\x00\x12\x11\n\rADMINISTRATOR\x10\x01\x12\r\n\tSECRETARY\x10\x02\x12\t\n\x05\x41GENT\x10\x03\x32\xf1\x02\n\x15\x41uthenticationService\x12\x34\n\x07\x41\x64\x64User\x12\x0e.services.User\x1a\x19.services.AddUserResponse\x12G\n\nUpdateUser\x12\x1b.services.UpdateUserMessage\x1a\x1c.services.UpdateUserResponse\x12:\n\nDeleteUser\x12\x0e.services.User\x1a\x1c.services.DeleteUserResponse\x12Q\n\x0c\x41uthenticate\x12\x1f.services.AuthenticationMessage\x1a .services.AuthenticationResponse\x12J\n\x0bVerifyToken\x12\x1c.services.VerifyTokenMessage\x1a\x1d.services.VerifyTokenResponse2\xe3\x06\n\x12TransactionService\x12S\n\x0e\x41\x64\x64Transaction\x12\x1f.services.AddTransactionMessage\x1a .services.AddTransactionResponse\x12\\\n\x11UpdateTransaction\x12\".services.UpdateTransactionMessage\x1a#.services.UpdateTransactionResponse\x12\\\n\x11\x44\x65leteTransaction\x12\".services.DeleteTransactionMessage\x1a#.services.DeleteTransactionResponse\x12\x44\n\tAddResult\x12\x1a.services.AddResultMessage\x1a\x1b.services.AddResultResponse\x12M\n\x0cUpdateResult\x12\x1d.services.UpdateResultMessage\x1a\x1e.services.UpdateResultResponse\x12M\n\x0c\x44\x65leteResult\x12\x1d.services.DeleteResultMessage\x1a\x1e.services.DeleteResultResponse\x12J\n\x12GetAllTransactions\x12\x0e.services.User\x1a$.services.GetAllTransactionsResponse\x12T\n\x17\x46\x65tchTransactionsOfUser\x12\x0e.services.User\x1a).services.FetchTransactionsOfUserResponse\x12@\n\rGetAllResults\x12\x0e.services.User\x1a\x1f.services.GetAllResultsResponse\x12t\n\x19\x46\x65tchResultsOfTransaction\x12*.services.FetchResultsOfTransactionMessage\x1a+.services.FetchResultsOfTransactionResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'services_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ROLE']._serialized_start=3254
  _globals['_ROLE']._serialized_end=3316
  _globals['_USER']._serialized_start=61
  _globals['_USER']._serialized_end=150
  _globals['_ADDUSERRESPONSE']._serialized_start=152
  _globals['_ADDUSERRESPONSE']._serialized_end=240
  _globals['_UPDATEUSERMESSAGE']._serialized_start=242
  _globals['_UPDATEUSERMESSAGE']._serialized_end=339
  _globals['_UPDATEUSERRESPONSE']._serialized_start=341
  _globals['_UPDATEUSERRESPONSE']._serialized_end=432
  _globals['_DELETEUSERRESPONSE']._serialized_start=434
  _globals['_DELETEUSERRESPONSE']._serialized_end=494
  _globals['_AUTHENTICATIONMESSAGE']._serialized_start=496
  _globals['_AUTHENTICATIONMESSAGE']._serialized_end=555
  _globals['_AUTHENTICATIONRESPONSE']._serialized_start=557
  _globals['_AUTHENTICATIONRESPONSE']._serialized_end=666
  _globals['_VERIFYTOKENMESSAGE']._serialized_start=668
  _globals['_VERIFYTOKENMESSAGE']._serialized_end=733
  _globals['_VERIFYTOKENRESPONSE']._serialized_start=735
  _globals['_VERIFYTOKENRESPONSE']._serialized_end=773
  _globals['_TRANSACTION']._serialized_start=776
  _globals['_TRANSACTION']._serialized_end=981
  _globals['_TRANSACTION_STATUS']._serialized_start=930
  _globals['_TRANSACTION_STATUS']._serialized_end=981
  _globals['_ADDTRANSACTIONMESSAGE']._serialized_start=983
  _globals['_ADDTRANSACTIONMESSAGE']._serialized_end=1080
  _globals['_ADDTRANSACTIONRESPONSE']._serialized_start=1082
  _globals['_ADDTRANSACTIONRESPONSE']._serialized_end=1191
  _globals['_UPDATETRANSACTIONMESSAGE']._serialized_start=1194
  _globals['_UPDATETRANSACTIONMESSAGE']._serialized_end=1356
  _globals['_UPDATETRANSACTIONRESPONSE']._serialized_start=1359
  _globals['_UPDATETRANSACTIONRESPONSE']._serialized_end=1501
  _globals['_DELETETRANSACTIONMESSAGE']._serialized_start=1503
  _globals['_DELETETRANSACTIONMESSAGE']._serialized_end=1603
  _globals['_DELETETRANSACTIONRESPONSE']._serialized_start=1605
  _globals['_DELETETRANSACTIONRESPONSE']._serialized_end=1672
  _globals['_RESULT']._serialized_start=1675
  _globals['_RESULT']._serialized_end=1816
  _globals['_ADDRESULTMESSAGE']._serialized_start=1818
  _globals['_ADDRESULTMESSAGE']._serialized_end=1944
  _globals['_ADDRESULTRESPONSE']._serialized_start=1946
  _globals['_ADDRESULTRESPONSE']._serialized_end=2040
  _globals['_UPDATERESULTMESSAGE']._serialized_start=2043
  _globals['_UPDATERESULTMESSAGE']._serialized_end=2224
  _globals['_UPDATERESULTRESPONSE']._serialized_start=2226
  _globals['_UPDATERESULTRESPONSE']._serialized_end=2353
  _globals['_DELETERESULTMESSAGE']._serialized_start=2356
  _globals['_DELETERESULTMESSAGE']._serialized_end=2485
  _globals['_DELETERESULTRESPONSE']._serialized_start=2487
  _globals['_DELETERESULTRESPONSE']._serialized_end=2549
  _globals['_FETCHTRANSACTIONSOFUSERRESPONSE']._serialized_start=2552
  _globals['_FETCHTRANSACTIONSOFUSERRESPONSE']._serialized_end=2700
  _globals['_GETALLTRANSACTIONSRESPONSE']._serialized_start=2703
  _globals['_GETALLTRANSACTIONSRESPONSE']._serialized_end=2846
  _globals['_FETCHRESULTSOFTRANSACTIONMESSAGE']._serialized_start=2848
  _globals['_FETCHRESULTSOFTRANSACTIONMESSAGE']._serialized_end=2956
  _globals['_FETCHRESULTSOFTRANSACTIONRESPONSE']._serialized_start=2958
  _globals['_FETCHRESULTSOFTRANSACTIONRESPONSE']._serialized_end=3067
  _globals['_GETALLRESULTSMESSAGE']._serialized_start=3069
  _globals['_GETALLRESULTSMESSAGE']._serialized_end=3121
  _globals['_GETALLRESULTSRESPONSE']._serialized_start=3124
  _globals['_GETALLRESULTSRESPONSE']._serialized_end=3252
  _globals['_AUTHENTICATIONSERVICE']._serialized_start=3319
  _globals['_AUTHENTICATIONSERVICE']._serialized_end=3688
  _globals['_TRANSACTIONSERVICE']._serialized_start=3691
  _globals['_TRANSACTIONSERVICE']._serialized_end=4558
# @@protoc_insertion_point(module_scope)
