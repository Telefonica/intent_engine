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
    return __addr+":"+__port

# Create a function to send a CreateNetwork request
def create_network(stub,data):
    
    # Create a CreateNetworkRequest object
    request = CreateNetworkRequest(**data)

    # Send the request and get the response from the server
    response = stub.CreateNetwork(request)
    print("CreateNetworkResponse:", response.message)

# Create a function to send a DeleteNetwork request
def delete_network(stub,data):
    request = DeleteNetworkRequest(network_name="ExampleNetwork")

    # Send the request and get the response
    response = stub.DeleteNetwork(request)
    print("DeleteNetworkResponse:", response.message)

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

    # Send the request and get the response
    response = stub.CreateOverlay(request)
    print("CreateOverlayResponse:", response.message)

# Main function to run the client
def run(params,data):

    # Connect to the gRPC server (assumed running on localhost:50051)
    with grpc.insecure_channel(get_l2smmd_enviroment()) as channel:
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

if __name__ == "__main__":
    run()