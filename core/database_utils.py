from devtools import pprint
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import XSD
import logging
from rdflib.plugins.stores import sparqlstore

logger = logging.getLogger(__name__)
def create_intent_graph(intent_model):
    # Define namespaces
    EX = Namespace("http://example.org/")

    # Create a Graph
    g = Graph()

    # Extract intent data from intent_model
    intent = intent_model.get_intent()
    intent_dict = intent.dict(exclude_defaults=True)

    # Create URIRefs for the intent and its properties
    intent_uri = URIRef(f"http://example.org/intent/{intent_dict['id']}")
    g.add((intent_uri, RDF.type, EX.Intent))
    g.add((intent_uri, EX.userLabel, Literal(intent_dict['userLabel'], datatype=XSD.string)))
    g.add((intent_uri, EX.intentPriority, Literal(intent_dict['intentPriority'], datatype=XSD.int)))
    g.add((intent_uri, EX.observationPeriod, Literal(intent_dict['observationPeriod'], datatype=XSD.int)))
    g.add((intent_uri, EX.intentAdminState, Literal(intent_dict['intentAdminState'], datatype=XSD.string)))

    # Add intent expectations
    for exp in intent_dict['intentExpectations']:
        exp_uri = URIRef(f"http://example.org/intent/{intent_dict['id']}/expectation/{exp['expectationId']}")
        g.add((exp_uri, RDF.type, EX.Expectation))
        g.add((exp_uri, EX.expectationVerb, Literal(exp['expectationVerb'], datatype=XSD.string)))
        g.add((exp_uri, EX.objectType, Literal(exp['expectationObject']['objectType'], datatype=XSD.string)))
        g.add((exp_uri, EX.objectInstance, Literal(exp['expectationObject']['objectInstance'], datatype=XSD.string)))

        # Link intent to expectation
        g.add((intent_uri, EX.intentExpectation, exp_uri))
        
        # Add object contexts
        for ctx in exp['expectationObject']['objectContexts']:
            ctx_uri = URIRef(f"http://example.org/intent/{intent_dict['id']}/expectation/{exp['expectationId']}/context/{ctx['contextAttribute']}")
            g.add((ctx_uri, RDF.type, EX.Context))
            g.add((ctx_uri, EX.contextAttribute, Literal(ctx['contextAttribute'], datatype=XSD.string)))
            g.add((ctx_uri, EX.contextCondition, Literal(ctx['contextCondition'], datatype=XSD.string)))
            g.add((ctx_uri, EX.contextValueRange, Literal(ctx['contextValueRange'], datatype=XSD.string)))

            # Link expectation to context
            g.add((exp_uri, EX.intentContext, ctx_uri))

        # Add expectation targets
        if 'expectationTargets' in exp:
            for tgt in exp['expectationTargets']:
                tgt_uri = URIRef(f"http://example.org/intent/{intent_dict['id']}/expectation/{exp['expectationId']}/target/{tgt['targetName']}")
                g.add((tgt_uri, RDF.type, EX.Target))
                g.add((tgt_uri, EX.targetName, Literal(tgt['targetName'], datatype=XSD.string)))
                g.add((tgt_uri, EX.targetCondition, Literal(tgt['targetCondition'], datatype=XSD.string)))
                g.add((tgt_uri, EX.targetValueRange, Literal(tgt['targetValueRange'], datatype=XSD.string)))

                # Link expectation to context
                g.add((intent_uri, EX.intentTarget, tgt_uri))

                # Add target contexts
                if 'targetContexts' in tgt:
                    for tgt_ctx in tgt['targetContexts']:
                        tgt_ctx_uri = URIRef(f"http://example.org/intent/{intent_dict['id']}/expectation/{exp['expectationId']}/target/{tgt['targetName']}/context/{tgt_ctx['contextAttribute']}")
                        g.add((tgt_ctx_uri, RDF.type, EX.Context))
                        g.add((tgt_ctx_uri, EX.contextAttribute, Literal(tgt_ctx['contextAttribute'], datatype=XSD.string)))
                        g.add((tgt_ctx_uri, EX.contextCondition, Literal(tgt_ctx['contextCondition'], datatype=XSD.string)))
                        g.add((tgt_ctx_uri, EX.contextValueRange, Literal(tgt_ctx['contextValueRange'], datatype=XSD.string)))

                        # Link contextTarget to Target
                        g.add((tgt_uri, EX.targetContext, tgt_ctx_uri))

    # Add intent contexts
    for ctx in intent_dict['intentContexts']:
        ctx_uri = URIRef(f"http://example.org/intent/{intent_dict['id']}/context/{ctx['contextAttribute']}")
        g.add((ctx_uri, RDF.type, EX.Context))
        g.add((ctx_uri, EX.contextAttribute, Literal(ctx['contextAttribute'], datatype=XSD.string)))
        g.add((ctx_uri, EX.contextCondition, Literal(ctx['contextCondition'], datatype=XSD.string)))
        g.add((ctx_uri, EX.contextValueRange, Literal(ctx['contextValueRange'], datatype=XSD.string)))

        # Link contextTarget to Target
        g.add((intent_uri, EX.intentContext, ctx_uri))


    # Serialize the graph to a file (optional)
    g.serialize(destination="intent.rdf", format="turtle")

    # Print the graph in Turtle format
    pprint(g.serialize(format="turtle").encode("utf-8"))

    return g

# def store_graph_in_file(graph, file_path):
#     graph.serialize(destination=file_path, format="turtle")

def store_graph_in_graphdb(graph, endpoint_url, repository_id):

    store = sparqlstore.SPARQLUpdateStore()
    store.open((f"{endpoint_url}/repositories/{repository_id}", f"{endpoint_url}/repositories/{repository_id}/statements"))
    
    for triple in graph:
        store.add(triple)

    # # Example usage:
    # # Store graph in a file
    # store_graph_in_file(g, "/path/to/your/file.ttl")

    # # Store graph in a GraphDB database
    # store_graph_in_graphdb(g, "http://localhost:7200", "your_repository_id")