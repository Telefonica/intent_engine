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
import logging
from devtools import pprint
import requests
from rdflib import BNode, ConjunctiveGraph,RDF, XSD, RDFS,FOAF
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import Namespace
from intent_engine.tools.enums import ComparisonType
# import sys
# sys.path.insert(1, '/home/ubuntu/Repos/intent_engine/tool')
from intent_engine.core.ib_model import IntentModel

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


base_folder = "data"
product_path = "intent_engine/tools/data/example_1.ttl"
# product_path = "intent_engine/tools/data/ran_intent.ttl"

# TODO: import namespaces like default
nLOG=Namespace("http://example.org/log#")
nLOG.allOf
nLOG.oneOf
nLOG.anyOf
nLOG.noneOf

nICM=Namespace("http://example.org/icm#")
nICM.Intent
nICM.DeliveryExpectation
nICM.PropertyExpectation
nICM.target
nICM.deliveryType
nICM.Target
nICM.chooseFrom
nICM.Condition
nICM.intersection

nQUAN=Namespace("http://example.org/quan#")
nQUAN.smaller
nQUAN.greater


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

def traverse_rdf_list(graph, start_node):
    """Traverse an RDF list starting from `start_node`."""
    items = []
    current_node = start_node
    
    while current_node and current_node != RDF.nil:
        first_item = graph.value(current_node, RDF.first)
        rest_node = graph.value(current_node, RDF.rest)
        
        if first_item:
            items.append(first_item)
        
        current_node = rest_node
    
    return items

def get_bnode_values_recursive(graph, node):
    """Recursively retrieve all properties and values for a given node."""
    if isinstance(node, BNode):
        values = {}
        
        for predicate, obj in graph.predicate_objects(subject=node):
            if isinstance(obj, BNode):
                values[predicate] = get_bnode_values_recursive(graph, obj)
            else:
                values[predicate] = obj
        
        return values
    elif isinstance(node, URIRef) or isinstance(node, Literal):
        return node
    else:
        return None

def get_bnode_values(graph, bnode):
    """Retrieve all properties and values for a given blank node."""
    values = {}
    
    for predicate, obj in graph.predicate_objects(subject=bnode):
        values['predicate'] = predicate
        values['object'] = obj
    
    return values

def make_graph_from_nquads(input_data,identifier):
    g = ConjunctiveGraph(identifier=identifier)
    data = open(input_data, "rb")
    g.parse(data, format="turtle")

    return g

def format_node(node):
    if isinstance(node, URIRef):
        return node.split('/')[-1] if '/' in node else node.split('#')[-1]
    elif isinstance(node, BNode):
        return str(node)
    elif isinstance(node, Literal):
        return node.value
    else:
        return ""

# TODO: Asume is more than one intent
def get_intents(g : ConjunctiveGraph) -> list[URIRef]:
    """
    Get a list of intents of type icm:Intent.
    3GPP: Intent
    Return: list[URIRef]
    """
    intents=[]
    for intent in g.subjects(object=nICM.Intent):
            # Es Intent
            logger.info("intent: %s",format_node(intent))
            intents.append(intent)
    return intents

def get_intent_expectations(g : ConjunctiveGraph, intent_subject) -> tuple[list[URIRef],URIRef]:
    """
    Get the list of Expectations. They can be of subclasses icm:DeliveryExpectation, 
    icm:PropertyExpectation and icm:ReportingExpectation. Also, returns the predicate
    describing how to handle the list of Expectations.
    3GPP: depends on subclass
    Return: list[URIRef], URIRef (log:)
    """
    for predicate in g.predicates(subject=intent_subject):
        if predicate!=RDF.type:
            pred=predicate

    # Cases nLOG
    for predicate,expectation_list in g.predicate_objects(subject=intent_subject):
        if predicate!=RDF.type:
            # Expectations log:
            print("expectationList: ",expectation_list)
            list_items = traverse_rdf_list(g, expectation_list)
            # Print the items in the list
            for item in list_items:
                print(format_node(item))
    return list_items,pred

def get_delivery_expectations(g : ConjunctiveGraph, intent_subject) -> list[URIRef]:
    """
    Get the objects with class icm:DeliveryExpectaion with given intent
    as a subject.
    3GPP: expectationObject
    Return: list[URIRef]  
    """
    expectations,predicates=get_intent_expectations(g,intent_subject)
    delivery_expectations=[]
    for item in expectations:
        print("deb",g.objects(subject=item, predicate=RDF.type))
        # Deliver expectation case
        if nICM.DeliveryExpectation==g.value(subject=item, predicate=RDF.type):
            print("Deliver: ",item)
            delivery_expectations.append(item)
    return delivery_expectations

def get_delivery_target_and_type(g : ConjunctiveGraph, delivery_subject)->tuple[URIRef,URIRef]:
    """
    Given a subject of a icm:DeliveryExpectation, get its icm:target. Also,
    get the icm:deliveryType of the expectation.
    3GPP: objectContext, objectType
    Return: URIRef, URIRef.
    """
    targets=[]
    # 3GPP: objectType
    delivery_type=g.value(subject=delivery_subject, predicate=nICM.deliveryType)
    print("type ",delivery_type)

    # 3GPP: objectContext
    for target in g.objects(subject=delivery_subject, predicate=nICM.target):
        print("target ",target)
        targets.append(target)
    # Pnly one target per exp_delivery?
    return targets,delivery_type

def get_target_members(g : ConjunctiveGraph, target_subject) -> tuple[list[URIRef],URIRef]:
    """
    Get the rdfs:member or icm:chooseFrom list of a subject with class a icm:Target. Also,
    returns the predicate that describe the object.
    3GPP: contextAttribute, contextCondition, contextValueRange
    Return: list[URIRef], URIRef
    """
    bnode_values=[]
    predicate=None
    label_target={}
    if nICM.Target==g.value(subject=target_subject, predicate=RDF.type):
        for pred,obj in g.predicate_objects(subject=target_subject):
            logger.debug("counting targets %s", obj)
            if obj != nICM.Target:
                # Posible target types or constructions
                if pred==nICM.chooseFrom:
                    # List to choose
                    print("target %s compose by chooseFrom",target_subject)
                    predicate=pred
                    target_context=traverse_rdf_list(g,obj)
                    print("obj ",target_context)
                    for node in target_context:
                        if isinstance(node,BNode):
                            bnode_value = get_bnode_values(g, node)
                            bnode_values.append(bnode_value)
                            # TODO: check posibilities
                            print("bnode_values ",bnode_value)
                if pred==RDFS.member:
                    print("target %s compose by members",target_subject)
                    predicate=pred
                    # target_context=traverse_rdf_list(g,obj)
                    print("obj ",obj)
                    bnode_values.append(obj)
                if pred==RDFS.label:
                    print("target %s compose by string label",target_subject)
                    predicate=pred
                    # target_context=traverse_rdf_list(g,obj)
                    label_target['predicate']=target_subject
                    label_target['object']=obj
                    print("value ",obj)
                    bnode_values.append(label_target)


    return bnode_values,predicate
    
def get_property_expectation(g : ConjunctiveGraph,intent_subject) -> list[URIRef]:
    """
    Get the expextation of class icm:PropertyExpectation.
    3GPP: expectationTargets
    Return: list[URIRef]
    """
    expectations,predicates=get_intent_expectations(g,intent_subject)
    property_expectations=[]
    for item in expectations:
        print("deb",g.objects(subject=item, predicate=RDF.type))
        # Property expectation case
        if nICM.PropertyExpectation==g.value(subject=item, predicate=RDF.type):
            print("Property: ",item)
            property_expectations.append(item)
            
    return property_expectations

def get_property_expectation_target(g : ConjunctiveGraph,expectation_subject) -> URIRef:
    """
    Get the icm:target of a icm:PropertyExpectation class. This could also work
    with any other Expectation as is a subclass. 
    3GPP: targetContext
    Return: URIRef
    """
    # targetContext
    target_context=g.value(subject=expectation_subject,predicate=nICM.target)
    print("target_context ",target_context)
    return target_context

def get_property_expectation_members(g : ConjunctiveGraph,expectation_subject):
    """
    Get list of conditions form the icm:PropertyExpectation class. Also, return
    de predicate that describe how to handle the list of conditions.
    3GPP: expectationTarget(targetName)
    Retrun: list[URIRef], URIRef (log:)
    """
    for predicate in g.predicates(subject=expectation_subject):
        if predicate!=RDF.type:
            pred=predicate

    # TODO: check other log posibilities
    exps=g.value(subject=expectation_subject,predicate=nLOG.allOf)
    target_names=[]
    for exp_target in traverse_rdf_list(g,exps):
        # for each expectationTarget
        print("target_name",exp_target)
        target_names.append(exp_target)
    return target_names,pred

def get_condition_value(g : ConjunctiveGraph,condition)->tuple[list[URIRef],URIRef]:
    """
    Get a list of values and labels of a icm:Condition. Also, return the predicate describing
    how to handle the values.
    3GPP: targetCondition,targetValueRange
    Return: list[URIRef],URIRef (quan:)
    """
    # targetCondition
    values=[]
    target_name=None
    pred=None
    for p in g.predicates(subject=condition):
        if p!=RDF.type:
            pred=p
    for pred,obj in g.predicate_objects(subject=condition):
        print("condition",pred)
        if nICM.Condition==obj and pred==RDF.type:
            print("Is icm:Condition")
        else:
            # Condition cases?
            if pred==nQUAN.smaller:
                print("Smaller than")
            print("obj",traverse_rdf_list(g,obj))
            for item in traverse_rdf_list(g,obj):
                # Range if several items
                if isinstance(item,BNode):
                    nodes=get_bnode_values_recursive(g,item)
                    print("nodes: ",nodes)
                    # valueRange for target
                    print("value: ", nodes[RDF.value])
                    print("label: ", nodes[RDFS.label])
                    values.append(nodes)
                elif isinstance(item,URIRef):
                    print("target_name",item)
                    target_name=item
                    # nodes['name']=item
                    # values.append(nodes)
    return values,pred,target_name

def rdf_to_3gpp_condition(rdf) -> ComparisonType:
    
    match format_node(rdf):
        case "icm#chooseFrom":
            return ComparisonType.IS_ONE_OF.name
        case "quan#smaller":
            return ComparisonType.IS_LESS_THAN.name
        case _:
            return ComparisonType.IS_EQUAL_TO.name

def generate_id():
    return 
    
if __name__=="__main__":
    
    g = make_graph_from_nquads(product_path,"RAN_Intent")
    print(g.serialize(format="turtle"))
    print("RDF to 3GPP translation...")
    # --- 3gpp intent construction ----
    intent_expectations=[]
    object_contexts=[]
    expectation_targets=[]
    # ---------------------------------
    intents=get_intents(g)
    logger.info("intents: %s",intents)
    for intent in intents:
        expectations,predicates=get_intent_expectations(g=g,intent_subject=intent)
        logger.info("expectations: %s",expectations)
        delivery_expectations=get_delivery_expectations(g=g,intent_subject=intent)
        logger.info("delivery_expectations: %s",delivery_expectations)
        property_expectations=get_property_expectation(g,intent)
        logger.info("property_expectations: %s",property_expectations)

        # --- 3gpp intent construction ----
        # Only deliver case when something(delivery_type) needs to be deliver
        expectation_verb='ENSURE'
        # ---------------------------------

        for delivery_expectation in delivery_expectations:
            # Target list inside an object, several targets are possible and have to be fulfilled all
            delivery_targets,delivery_type=get_delivery_target_and_type(g=g,delivery_subject=delivery_expectation)
            logger.info("Target: %s ,type: %s",delivery_targets,delivery_type)
            for delivery_target in delivery_targets:
                # Members in target are the different valueRange attributes in 3gpp
                deliv_trg_members,deliv_trg_predicate=get_target_members(g,target_subject=delivery_target)
            
            logger.info("Members: %s, predicate: %s",deliv_trg_members,deliv_trg_predicate)

            # --- 3gpp intent construction ----
            # Aqui hay que tener en cuenta si es choose from or all of
            # Si uno lista, si otro valores
            expectation_verb='DELIVER'
            for deliv_trg in deliv_trg_members:
                logger.debug("deliv_trg_ %s", deliv_trg)
                object_context={
                                "contextAttribute": format_node(deliv_trg['predicate']),
                                "contextCondition": rdf_to_3gpp_condition(deliv_trg_predicate),
                                "contextValueRange": format_node(deliv_trg['object'])
                                }
                object_contexts.append(object_context)

            expectation_object={
                            "objectType": format_node(delivery_type),
                            "objectInstance": format_node(delivery_expectation),
                            "objectContexts": object_contexts
                        }
            # ---------------------------------
        
        for property_expectation in property_expectations:
            conditions,trg_predicate=get_property_expectation_members(g=g,expectation_subject=property_expectation)
            logger.info("conditions: %s, trg_predicate: %s",conditions,trg_predicate)
            property_target=get_property_expectation_target(g=g,expectation_subject=property_expectation)
            logger.info("property_target: %s",property_target)
            target_member,member_pred=get_target_members(g=g,target_subject=property_target)
            o=[logger.info("target_member: %s",format_node(trg_memb)) for trg_memb in target_member]
            for condition in conditions:
                value,comparator,target_name=get_condition_value(g=g,condition=condition)
                o=[logger.info("value: %s %s, predicate: %s",v[RDF.value],v[RDFS.label],format_node(comparator))
                   for v in value]

                # --- 3gpp intent construction ----
                # format_node(v[RDF.value]) -> str(v[RDF.value]) to avoid decimal word
                value_labels=[(format_node(v[RDF.value]),format_node(v[RDFS.label])) for v in value]
                if target_name:
                    target_name_3gpp=format_node(target_name)
                else:
                    target_name_3gpp=format_node(condition)
                expectation_target={
                                    "targetName": target_name_3gpp,
                                    "targetCondition": rdf_to_3gpp_condition(comparator),
                                    "targetValueRange": str(value_labels),
                                    "targetContext": {}
                                }
                logger.debug("expectation targets %s",expectation_target)
                expectation_targets.append(expectation_target)
                # ---------------------------------

        
        intent_expectation={
                        "expectationId": "",
                        "expectationVerb": expectation_verb,
                        "expectationObject": expectation_object,
                        "expectationTargets": expectation_targets
                    }
        intent_expectations.append(intent_expectation)
        intent_model={
                "Intent": {
                    "id": "1",
                    "userLabel": format_node(intent),
                    "intentExpectations": intent_expectations,
                    # "intentContexts": [
                    # {
                    #     "contextAttribute": "",
                    #     "contextCondition": "",
                    #     "contextValueRange": ""
                    # }
                    # ],
                    "intentPriority": 1,
                    "observationPeriod": 60,
                    "intentAdminState": "ACTIVATED"
                }
            }
        pprint(intent_model)
        intent=IntentModel(intent_model)