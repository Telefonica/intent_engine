# Generate Python code
python3 -m grpc_tools.protoc -I=intent_engine/executioners/grpc_libs/proto/ --python_out=intent_engine/executioners/grpc_libs/generated/ --grpc_python_out=intent_engine/executioners/grpc_libs/generated/ --pyi_out=intent_engine/executioners/grpc_libs/generated/ intent_engine/executioners/grpc_libs/proto/*.proto

# new line added to generate protobuf for the `grpclib` library
python3 -m grpc_tools.protoc -I=intent_engine/executioners/grpc_libs/proto/ --python_out=intent_engine/executioners/grpc_libs/generated/asyncio --grpclib_python_out=intent_engine/executioners/grpc_libs/generated/asyncio intent_engine/executioners/grpc_libs/proto/*.proto

# Arrange generated code imports to enable imports from arbitrary subpackages
find intent_engine/executioners/grpc_libs/generated/ -type f -iname *.py -exec sed -i -E 's/(import\ .*)_pb2/from . \1_pb2/g' {} \;