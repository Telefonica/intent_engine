import os
import requests
from rdflib import ConjunctiveGraph

base_folder = "data"
# products_url = "http://data.dws.informatik.uni-mannheim.de/structureddata/2014-12/quads/ClassSpecificQuads/schemaorgProduct.nq.sample.txt"
product_path = "example.trig"


def download_data(dir_path, data_url, data_path):
    """
    Convenience function that uses the requests library to retrieve data
    given a url to the dataset and a directory folder on your computer.
    """
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    response = requests.get(data_url)
    with open(os.path.join(dir_path, data_path), "wb") as f:
        f.write(response.content)

    return data_path

def make_graph_from_nquads(input_data):
    g = ConjunctiveGraph(identifier="RAN_Intent")
    data = open(input_data, "rb")
    g.parse(data, format="turtle")

    return g

# download_data(base_folder, products_url, product_path)

with open(os.path.join(base_folder, product_path), "rb") as input_data:
    for i in range(5):
        print(input_data.readline())
        print("")



g = make_graph_from_nquads(os.path.join(base_folder, product_path))

# for quad in g.quads():
#     print(quad)
#     print("")

# from rdflib import BNode, URIRef

# target_node = BNode('N01d9696afdba4f7aab73c45c17ea2337')
# keyword_ref = URIRef('http://schema.org/ImageObject/keywords')

# keywords = [
#     str(keyword) for bnode, linkage, keyword, product_uri
#     in g.quads((target_node, keyword_ref, None, None))
# ]

# print(list(keywords))

# image_ref = URIRef("http://schema.org/Product/image")

# images = [
#     image for bnode, linkage, image, product_uri
#     in g.quads((None, image_ref, None, None))
# ]

# from rdflib import Graph
# g = Graph()
# g.parse('http://dbpedia.org/resource/Semantic_Web')

# for s, p, o in g:
#     print(s, p, o)

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDFS, XSD,FOAF

# g = Graph()
# semweb = URIRef('http://dbpedia.org/resource/Semantic_Web')
# type = g.value(semweb, RDFS.label)

# g.add((
#     URIRef("http://example.com/person/nick"),
#     FOAF.givenName,
#     Literal("Nick", datatype=XSD.string)
# ))

print(g.serialize(format="turtle"))

from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
import networkx as nx
import matplotlib.pyplot as plt

G = rdflib_to_networkx_multidigraph(g)

# Plot Networkx instance of RDF Graph
pos = nx.spring_layout(G, scale=2)
edge_labels = nx.get_edge_attributes(G, 'r')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
nx.draw(G, with_labels=True)

#if not in interactive mode for 
plt.show()

# Query the data in g using SPARQL
# This query returns the 'name' of all ``foaf:Person`` instances
q = """
    PREFIX ex: <http://example.org/>

    SELECT ?Intent
    WHERE {
        ?p rdf:type icm:Target .

        
    }
"""
# ?p ex:Exp1_delivery ?Intent .
# Apply the query to the graph and iterate through results
for r in g.query(q):
    print(r)