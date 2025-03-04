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

def get_intent_from_userLabel(userLabel, endpoint_url, repository_id):
    """
    Return the full intent stored in the RDF graph matching the userLabel.
    """
    # Define namespaces
    EX = Namespace("http://example.org/")
    g = sparqlstore.SPARQLUpdateStore()
    g.open((f"{endpoint_url}/repositories/{repository_id}", f"{endpoint_url}/repositories/{repository_id}/statements"))

    # Find the intent with the given userLabel
    intent_uri = None
    for (s, p, o),_ in g.triples((None, EX.userLabel, Literal(userLabel))):
        if p == EX.userLabel and str(o) == userLabel:
            intent_uri = s
            break
    
    logger.debug("Intent URI matching userLabel %s: %s",userLabel, intent_uri)
    if intent_uri is None:
        return None

    return intent_uri

def get_intent_from_uri(intent_uri, endpoint_url, repository_id):
    """
    Return the full intent stored in the RDF graph matching the intent URI.
    """
    intent_data = {
        "intent": {
            "id": intent_uri.split("/")[-1],
            "userLabel": None,
            "intentPriority": None,
            "observationPeriod": None,
            "intentAdminState": None,
            "intentExpectations": [],
            "intentContexts": []
        }
    }

    # Populate the intent data
    for pred, obj in g.predicate_objects(intent_uri):
        if pred == EX.intentPriority:
            intent_data["intent"]["intentPriority"] = int(obj)
        elif pred == EX.observationPeriod:
            intent_data["intent"]["observationPeriod"] = int(obj)
        elif pred == EX.intentAdminState:
            intent_data["intent"]["intentAdminState"] = str(obj)
        elif pred == EX.intentExpectation:
            expectation_data = {
                "expectationId": obj.split("/")[-1],
                "expectationVerb": None,
                "expectationObject": {
                    "objectType": None,
                    "objectInstance": None,
                    "objectContexts": []
                },
                "expectationTargets": []
            }
            for exp_pred, exp_obj in g.predicate_objects(obj):
                if exp_pred == EX.expectationVerb:
                    expectation_data["expectationVerb"] = str(exp_obj)
                elif exp_pred == EX.objectType:
                    expectation_data["expectationObject"]["objectType"] = str(exp_obj)
                elif exp_pred == EX.objectInstance:
                    expectation_data["expectationObject"]["objectInstance"] = str(exp_obj)
                elif exp_pred == EX.intentContext:
                    context_data = {
                        "contextAttribute": None,
                        "contextCondition": None,
                        "contextValueRange": None
                    }
                    for ctx_pred, ctx_obj in g.predicate_objects(exp_obj):
                        if ctx_pred == EX.contextAttribute:
                            context_data["contextAttribute"] = str(ctx_obj)
                        elif ctx_pred == EX.contextCondition:
                            context_data["contextCondition"] = str(ctx_obj)
                        elif ctx_pred == EX.contextValueRange:
                            context_data["contextValueRange"] = str(ctx_obj)
                    expectation_data["expectationObject"]["objectContexts"].append(context_data)
            intent_data["intent"]["intentExpectations"].append(expectation_data)
        elif pred == EX.intentContext:
            context_data = {
                "contextAttribute": None,
                "contextCondition": None,
                "contextValueRange": None
            }
            for ctx_pred, ctx_obj in g.predicate_objects(obj):
                if ctx_pred == EX.contextAttribute:
                    context_data["contextAttribute"] = str(ctx_obj)
                elif ctx_pred == EX.contextCondition:
                    context_data["contextCondition"] = str(ctx_obj)
                elif ctx_pred == EX.contextValueRange:
                    context_data["contextValueRange"] = str(ctx_obj)
            intent_data["intent"]["intentContexts"].append(context_data)
        elif pred == EX.intentTarget:
            target_data = {
                "targetName": None,
                "targetCondition": None,
                "targetValueRange": None,
                "targetContexts": []
            }
            for tgt_pred, tgt_obj in g.predicate_objects(obj):
                if tgt_pred == EX.targetName:
                    target_data["targetName"] = str(tgt_obj)
                elif tgt_pred == EX.targetCondition:
                    target_data["targetCondition"] = str(tgt_obj)
                elif tgt_pred == EX.targetValueRange:
                    target_data["targetValueRange"] = str(tgt_obj)
                elif tgt_pred == EX.targetContext:
                    context_data = {
                        "contextAttribute": None,
                        "contextCondition": None,
                        "contextValueRange": None
                    }
                    for ctx_pred, ctx_obj in g.predicate_objects(tgt_obj):
                        if ctx_pred == EX.contextAttribute:
                            context_data["contextAttribute"] = str(ctx_obj)
                        elif ctx_pred == EX.contextCondition:
                            context_data["contextCondition"] = str(ctx_obj)
                        elif ctx_pred == EX.contextValueRange:
                            context_data["contextValueRange"] = str(ctx_obj)
                    target_data["targetContexts"].append(context_data)
            intent_data["intent"]["intentExpectations"][-1]["expectationTargets"].append(target_data)

    return intent_data

def get_intent_from_graph(intent,endpoint_url, repository_id):
    """
    Get the intent from a graph database using rdflib and store it in a dictionary.
    NOTE: Not tested yet
    """
    # loop through the graph and extract all the intents
    # Define namespaces
    EX = Namespace("http://example.org/")
    g = Graph(store=sparqlstore.SPARQLUpdateStore)
    g.open((f"{endpoint_url}/repositories/{repository_id}", f"{endpoint_url}/repositories/{repository_id}/statements"))
    # Query the graph for all intents
    query = """
    SELECT ?intent ?userLabel ?intentPriority ?observationPeriod ?intentAdminState
    WHERE {
        ?intent a EX.Intent ;
            EX.userLabel ?userLabel ;
            EX.intentPriority ?intentPriority ;
            EX.observationPeriod ?observationPeriod ;
            EX.intentAdminState ?intentAdminState .
    }
    """
    results = g.query(query)
    intents = []
    for result in results:
        intent_data = {
            "intent": {
                "id": result["intent"].split("/")[-1],
                "userLabel": result["userLabel"],
                "intentPriority": result["intentPriority"],
                "observationPeriod": result["observationPeriod"],
                "intentAdminState": result["intentAdminState"],
                "intentExpectations": [],
                "intentContexts": []
            }
        }
        # Query the graph for all expectations related to the intent
        query = f"""
        SELECT ?expectation ?expectationVerb ?objectType ?objectInstance
        WHERE {{
            ?intent EX.intentExpectation ?expectation .
            ?expectation EX.expectationVerb ?expectationVerb ;
                EX.objectType ?objectType ;
                EX.objectInstance ?objectInstance .
        }}
        """
        results = g.query(query)
        for result in results:
            expectation_data = {
                "expectationId": result["expectation"].split("/")[-1],
                "expectationVerb": result["expectationVerb"],
                "expectationObject": {
                    "objectType": result["objectType"],
                    "objectInstance": result["objectInstance"],
                    "objectContexts": []
                },
                "expectationTargets": []
            }
            # Query the graph for all contexts related to the expectation
            query = f"""
            SELECT ?context ?contextAttribute ?contextCondition ?contextValueRange
            WHERE {{
                ?expectation EX.intentContext ?context .
                ?context EX.contextAttribute ?contextAttribute ;
                    EX.contextCondition ?contextCondition ;
                    EX.contextValueRange ?contextValueRange .
            }}
            """
            results = g.query(query)
            for result in results:
                context_data = {
                    "contextAttribute": result["contextAttribute"],
                    "contextCondition": result["contextCondition"],
                    "contextValueRange": result["contextValueRange"]
                }
                expectation_data["expectationObject"]["objectContexts"].append(context_data)
            # Query the graph for all targets related to the expectation
            query = f"""
            SELECT ?target ?targetName ?targetCondition ?targetValueRange
            WHERE {{
                ?intent EX.intentTarget ?target .
                ?target EX.targetName ?targetName ;
                    EX.targetCondition ?targetCondition ;
                    EX.targetValueRange ?targetValueRange .
            }}
            """
            results = g.query(query)
            for result in results:
                target_data = {
                    "targetName": result["targetName"],
                    "targetCondition": result["targetCondition"],
                    "targetValueRange": result["targetValueRange"],
                    "targetContexts": []
                }
                # Query the graph for all contexts related to the target
                query = f"""
                SELECT ?context ?contextAttribute ?contextCondition ?contextValueRange
                WHERE {{
                    ?target EX.targetContext ?context .
                    ?context EX.contextAttribute ?contextAttribute ;
                        EX.contextCondition ?contextCondition ;
                        EX.contextValueRange ?contextValueRange .
                }}
                """
                results = g.query(query)
                for result in results:
                    context_data = {
                        "contextAttribute": result["contextAttribute"],
                        "contextCondition": result["contextCondition"],
                        "contextValueRange": result["contextValueRange"]
                    }
                    target_data["targetContexts"].append(context_data)
                expectation_data["expectationTargets"].append(target_data)
            intent_data["intent"]["intentExpectations"].append(expectation_data)
        # Query the graph for all contexts related to the intent
        query = f"""
        SELECT ?context ?contextAttribute ?contextCondition ?contextValueRange
        WHERE {{
            ?intent EX.intentContext ?context .
            ?context EX.contextAttribute ?contextAttribute ;
                EX.contextCondition ?contextCondition ;
                EX.contextValueRange ?contextValueRange .
        }}
        """
        results = g.query(query)
        for result in results:
            context_data = {
                "contextAttribute": result["contextAttribute"],
                "contextCondition": result["contextCondition"],
                "contextValueRange": result["contextValueRange"]
            }
            intent_data["intent"]["intentContexts"].append(context_data)
        intents.append(intent_data)
    return intents