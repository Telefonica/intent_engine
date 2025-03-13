# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import grpc
from concurrent import futures
from generated import l2smmd_pb2_grpc, l2smmd_pb2
import logging
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
# Implement the service
class L2SMMultiDomainServiceServicer(l2smmd_pb2_grpc.L2SMMultiDomainServiceServicer):
    def CreateNetwork(self, request, context):
        print(request)
        logger.info(request)
        return l2smmd_pb2.CreateNetworkResponse(message="Network created successfully!")

    def DeleteNetwork(self, request, context):
        logger.info(request)
        return l2smmd_pb2.DeleteNetworkResponse(message="Network deleted successfully!")

    def CreateOverlay(self, request, context):
        logger.info(request)
        return l2smmd_pb2.CreateOverlayResponse(message="Overlay created successfully!")

# Set up the gRPC server
def serve():

    logger.setLevel(level=logging.DEBUG)
    logger.info("Starting...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    l2smmd_pb2_grpc.add_L2SMMultiDomainServiceServicer_to_server(L2SMMultiDomainServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    logger.info("Server started on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    logger.setLevel(level=logging.DEBUG)
    logger.info("Running server...")
    serve()
