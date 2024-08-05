# © 2024 Telefónica Innovación Digital

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import requests
from rdflib import BNode, ConjunctiveGraph

cwd=os.getcwd()
base_folder = "tools/data"
# products_url = "http://data.dws.informatik.uni-mannheim.de/structureddata/2014-12/quads/ClassSpecificQuads/schemaorgProduct.nq.sample.txt"
product_path = "ran_intent.ttl"
print(os.path.join(cwd,base_folder, product_path))
full_path=os.path.join(cwd,base_folder, product_path)

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

with open(full_path, "rb") as input_data:
    for i in range(5):
        print(input_data.readline())
        print("")



g = make_graph_from_nquads(full_path)

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
# plt.show()
# Extract and format values
def format_node(node):
    if isinstance(node, URIRef):
        return node.split('/')[-1] if '/' in node else node.split('#')[-1]
    elif isinstance(node, BNode):
        return str(node)
    elif isinstance(node, Literal):
        return node.value
    else:
        return ""
# Query the data in g using SPARQL
# This query returns the 'name' of all ``foaf:Person`` instances
q = """
    PREFIX ex: <http://example.org/>
    PREFIX ex: <http://example.org/>
    PREFIX icm: <http://example.org/icm#>
    PREFIX log: <http://example.org/log#>
    PREFIX set: <http://example.org/set#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX quan: <http://example.org/quan#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT ?expectation ?cond ?lat ?p ?value
    WHERE {
    ex:RAN_Intent log:allOf ?list .
    ?list rdf:rest*/rdf:first ?expectation .
    OPTIONAL{
        ?expectation a icm:PropertyExpectation .
        ?expectation log:allOf ?explist .
        ?explist rdf:rest*/rdf:first ?cond .
            OPTIONAL{
            ?cond a icm:Condition .
            ?cond ?p ?olist .
            ?olist rdf:rest*/rdf:first ?valty .
            OPTIONAL{
                ?valty rdf:value ?value
            }
            }
        }

    }

"""
q2 = """
    SELECT ?expectation ?cond ?lat ?p ?value ?units
    WHERE {
    ex:RAN_Intent log:allOf ?list .
    ?list rdf:rest*/rdf:first ?expectation .
    OPTIONAL{
        ?expectation a icm:PropertyExpectation .
        ?expectation log:allOf ?explist .
        ?explist rdf:rest*/rdf:first ?cond .
            OPTIONAL{
            ?cond a icm:Condition .
            ?cond ?p ?olist .
            ?olist rdf:rest*/rdf:first ?valty .
            OPTIONAL{
                ?valty rdf:value ?value .
                ?valty rdfs:label ?units
            }
            }
        }

    }

"""
q3 = """
    SELECT ?expectation ?target ?attribute ?members ?condition ?value
    WHERE {
    ex:RAN_Intent log:allOf ?list .
    ?list rdf:rest*/rdf:first ?expectation .
    ?expectation a icm:DeliveryExpectation .
    ?expectation icm:Target ?target .
    ?expectation icm:deliveryType ?attribute .
    ?target icm:chooseFrom ?listTargets .
    ?listTargets rdf:rest*/rdf:first ?members .
        OPTIONAL{
            ?members ?condition ?value .
        }
    }

"""
print("Query")
for row in g.query(q3):
    expectation = row.expectation
    target = row.target
    attribute = row.attribute
    condition = row.condition if row.condition else ""
    value = row.value if row.value else ""

    expectation = format_node(expectation)
    target = format_node(target)
    attribute = format_node(attribute)
    condition = format_node(condition)
    value = format_node(value)

print(f"expectation: {expectation}, target: {target}, attribute: {attribute}, condition: {condition}, value: {value}")

print(f"En 3GPP:\n {expectation}, Context:\n AttributeName {target},\n attribute: {attribute},\n condition: {condition},\n value: {value}")

# Run the query and print the results without showing 'rdflib.term.Literal' or 'rdflib.term.URIRef'
# for row in g.query(q):
#     expectation = row.expectation
#     # Extract and format values
#     if isinstance(expectation, URIRef):
#         expectation = expectation.split('/')[-1] if '/' in expectation else expectation.split('#')[-1]

#     print(f"expectation: {expectation}")
# ?p ex:Exp1_delivery ?Intent .
# Apply the query to the graph and iterate through results

# for r in g.query(q3):
#     print(r)
# Run the query and print the results without showing 'rdflib.term.Literal' or 'rdflib.term.URIRef'
# for row in g.query(q2):
#     expectation = row.expectation
#     target = row.p
#     condition = row.cond
#     object_ = row.value
#     units = row.units
#     # Extract and format values
#     if isinstance(expectation, URIRef):
#         expectation = expectation.split('/')[-1] if '/' in expectation else expectation.split('#')[-1]
#     elif isinstance(expectation, BNode):
#         expectation = str(expectation)
#     if isinstance(target, URIRef):
#         target = target.split('/')[-1] if '/' in target else target.split('#')[-1]
#     if isinstance(condition, URIRef):
#         condition = condition.split('/')[-1] if '/' in condition else condition.split('#')[-1]
#     elif isinstance(condition, Literal):
#         condition = condition.value
#     elif isinstance(object_, BNode):
#         object_ = str(object_)
#     if isinstance(units, Literal):
#         units = str(units)

#     print(f"subject: {expectation}, predicate: {target}, object: {object_} {units}")