import grpc
from concurrent import futures
from generated import l2smmd_pb2_grpc, l2smmd_pb2
import logging
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
# Implement the service
class L2SMMultiDomainServiceServicer(l2smmd_pb2_grpc.L2SMMultiDomainServiceServicer):
    def CreateNetwork(self, request, context):
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
    logger.info("Server started on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
