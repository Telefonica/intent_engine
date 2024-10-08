import time
import grpc
from .generated.l2smmd_pb2 import ( Cluster, CreateNetworkRequest, CreateOverlayRequest, DeleteNetworkRequest, 
                                   L2Network, Link, OverlayTopology, Provider )# Import the generated protobuf message classes
from .generated import l2smmd_pb2_grpc  # Import the generated gRPC client stubs
import os
import logging
logger = logging.getLogger(__name__)

def get_l2smmd_enviroment():
    __addr=os.environ.get('GRPC_SERVICE_L2SM_ADDRESS')
    if(__addr):
        # Docker container case where hostname needed
        logger.debug("Reading enviroment GRPC_SERVICE_L2SM_ADDRESS vars: %s",__addr)
    else:
        __addr="l2sm-md-server.nemo-net.svc.cluster.local"

    __port=os.environ.get('GRPC_SERVICE_L2SM_PORT')
    if(__port):
        # Docker container case where hostname needed
        logger.debug("Reading enviroment GRPC_SERVICE_L2SM_PORT vars: %s",__port)
    else:
        __port="50051"
    logger.debug("Reading vars: %s",__addr+":"+__port)
    return __addr+":"+__port

# Function to create a gRPC channel with retry logic
def create_grpc_channel(target, max_retries=5, initial_delay=2):
    attempts = 0
    while attempts < max_retries:
        try:
            # Try to create a channel and test if it's ready
            channel = grpc.insecure_channel(target)
            grpc.channel_ready_future(channel).result(timeout=5)
            logger.info("Connected to gRPC server.")
            return channel
        except grpc.RpcError as e:
            attempts += 1
            logger.warning("Failed to connect to gRPC server (attempt %s/%s): %s",attempts,max_retries,e)
            if attempts >= max_retries:
                logger.warning("Maximum retry attempts reached. Giving up.")
                raise e  # Raise the exception if max retries are reached
            else:
                # Exponential backoff: wait longer before each retry
                delay = initial_delay * (2 ** (attempts - 1))
                logger.warning("Retrying in %s seconds...",delay)
                time.sleep(delay)
                
# Create a function to send a CreateNetwork request
def create_network(stub,data):
    
    # Create a CreateNetworkRequest object
    request = CreateNetworkRequest(**data)
    try:
        # Send the request and get the response from the server
        response = stub.CreateNetwork(request)
        logger.info("CreateNetworkResponse: %s", response.message)
    except grpc.RpcError as e:
        logger.warning("Failed to create network: %s",e)

# Create a function to send a DeleteNetwork request
def delete_network(stub,data):
    request = DeleteNetworkRequest(network_name="ExampleNetwork")

    try:
        # Send the request and get the response
        response = stub.DeleteNetwork(request)
        print("DeleteNetworkResponse:", response.message)
    except grpc.RpcError as e:
        print(f"Failed to delete network: {e}")

# Create a function to send a CreateOverlay request
def create_overlay(stub,data):
    # Create a provider
    provider = Provider(name="ExampleProvider", domain="example.com")

    # Create an OverlayTopology object
    overlay_topology = OverlayTopology(provider=provider)

    # Add clusters to the overlay
    cluster1 = Cluster(name="Cluster1")
    cluster2 = Cluster(name="Cluster2")
    overlay_topology.clusters.extend([cluster1, cluster2])

    # Add links between clusters
    link = Link(endpointA="Cluster1", endpointB="Cluster2")
    overlay_topology.links.append(link)

    # Create a CreateOverlayRequest object
    request = CreateOverlayRequest(overlay=overlay_topology)

    try:
        # Send the request and get the response
        response = stub.CreateOverlay(request)
        print("CreateOverlayResponse:", response.message)
    except grpc.RpcError as e:
        print(f"Failed to create overlay: {e}")

# Main function to run the client
def run(params,data):

    # Connect to the gRPC server (assumed running on localhost:50051)
    address_port=get_l2smmd_enviroment()
    try:
        # Create a channel with retry logic
        with create_grpc_channel(address_port) as channel:
            # Create a stub (client) using the generated gRPC classes
            stub = l2smmd_pb2_grpc.L2SMMultiDomainServiceStub(channel)

            # Call the different request functions
            match params['service']:
                case "create_network":
                    logger.info("Creating a network...")
                    create_network(stub,data)
                case "create_overlay":
                    logger.info("Creating an overlay...")
                    create_overlay(stub,data)
                case "delete_network":
                    logger.info("Deleting a network...")
                    delete_network(stub,data)

    except grpc.RpcError as e:
        print(f"Unable to establish a connection to the server: {e}")
    
if __name__ == "__main__":
    run()