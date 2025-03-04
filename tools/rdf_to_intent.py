import rdflib
import yaml

# Create a new RDF graph
g = rdflib.Graph()

# Parse the RDF Turtle data
turtle_data = """
<http://example.org/intent/1> a <http://example.org/Intent>;
  <http://example.org/intentAdminState> "ACTIVATED";
  <http://example.org/intentContext> <http://example.org/intent/1/context/EnergyEfficiency>,
    <http://example.org/intent/1/context/IsolationLevel>;
  <http://example.org/intentExpectation> <http://example.org/intent/1/expectation/1>,
    <http://example.org/intent/1/expectation/2>;
  <http://example.org/intentPriority> "1"^^<http://www.w3.org/2001/XMLSchema#int>;
  <http://example.org/intentTarget> <http://example.org/intent/1/expectation/1/target/DownlinkThroughputPerUE>,
    <http://example.org/intent/1/expectation/1/target/Latency>;
  <http://example.org/observationPeriod> "60"^^<http://www.w3.org/2001/XMLSchema#int>;
  <http://example.org/userLabel> "green_nest" .

<http://example.org/intent/1/context/EnergyEfficiency> a <http://example.org/Context>;
  <http://example.org/contextAttribute> "EnergyEfficiency";
  <http://example.org/contextCondition> "IS_EQUAL_TO_OR_GREATER_THAN";
  <http://example.org/contextValueRange> "90%" .

<http://example.org/intent/1/context/IsolationLevel> a <http://example.org/Context>;
  <http://example.org/contextAttribute> "IsolationLevel";
  <http://example.org/contextCondition> "IS_EQUAL_TO";
  <http://example.org/contextValueRange> "DedicatedResources" .

<http://example.org/intent/1/expectation/1> a <http://example.org/Expectation>;
  <http://example.org/expectationVerb> "DELIVER";
  <http://example.org/intentContext> <http://example.org/intent/1/expectation/1/context/AreaOfService>,
    <http://example.org/intent/1/expectation/1/context/ServiceType>;
  <http://example.org/objectInstance> "Slice_001";
  <http://example.org/objectType> "NEST" .

<http://example.org/intent/1/expectation/1/context/AreaOfService> a <http://example.org/Context>;
  <http://example.org/contextAttribute> "AreaOfService";
  <http://example.org/contextCondition> "IS_EQUAL_TO";
  <http://example.org/contextValueRange> "Urban" .

<http://example.org/intent/1/expectation/1/context/ServiceType> a <http://example.org/Context>;
  <http://example.org/contextAttribute> "ServiceType";
  <http://example.org/contextCondition> "IS_EQUAL_TO";
  <http://example.org/contextValueRange> "eMBB" .

<http://example.org/intent/1/expectation/1/target/DownlinkThroughputPerUE> a <http://example.org/Target>;
  <http://example.org/targetCondition> "IS_EQUAL_TO_OR_GREATER_THAN";
  <http://example.org/targetContext> <http://example.org/intent/1/expectation/1/target/DownlinkThroughputPerUE/context/TrafficPattern>;
  <http://example.org/targetName> "DownlinkThroughputPerUE";
  <http://example.org/targetValueRange> "1Gbps" .

<http://example.org/intent/1/expectation/1/target/DownlinkThroughputPerUE/context/TrafficPattern>
  a <http://example.org/Context>;
  <http://example.org/contextAttribute> "TrafficPattern";
  <http://example.org/contextCondition> "IS_EQUAL_TO";
  <http://example.org/contextValueRange> "HighUsagePeakHours" .

<http://example.org/intent/1/expectation/1/target/Latency> a <http://example.org/Target>;
  <http://example.org/targetCondition> "IS_EQUAL_TO_OR_LESS_THAN";
  <http://example.org/targetContext> <http://example.org/intent/1/expectation/1/target/Latency/context/TimeCriticality>;
  <http://example.org/targetName> "Latency";
  <http://example.org/targetValueRange> "10ms" .

<http://example.org/intent/1/expectation/1/target/Latency/context/TimeCriticality>
  a <http://example.org/Context>;
  <http://example.org/contextAttribute> "TimeCriticality";
  <http://example.org/contextCondition> "IS_EQUAL_TO";
  <http://example.org/contextValueRange> "High" .

<http://example.org/intent/1/expectation/2> a <http://example.org/Expectation>;
  <http://example.org/expectationVerb> "ENSURE";
  <http://example.org/intentContext> <http://example.org/intent/1/expectation/2/context/AreaOfService>,
    <http://example.org/intent/1/expectation/2/context/ServiceType>;
  <http://example.org/objectInstance> "Slice_002";
  <http://example.org/objectType> "NEST" .

<http://example.org/intent/1/expectation/2/context/AreaOfService> a <http://example.org/Context>;
  <http://example.org/contextAttribute> "AreaOfService";
  <http://example.org/contextCondition> "IS_EQUAL_TO";
  <http://example.org/contextValueRange> "Rural" .

<http://example.org/intent/1/expectation/2/context/ServiceType> a <http://example.org/Context>;
  <http://example.org/contextAttribute> "ServiceType";
  <http://example.org/contextCondition> "IS_EQUAL_TO";
  <http://example.org/contextValueRange> "mMTC" .
"""

g.parse(data=turtle_data, format="turtle")

# Create a dictionary to store the intent information
intent_data = {
    "intent": {
        "id": "1",
        "userLabel": None,
        "intentExpectations": [],
        "intentContexts": [],
        "adminState": None,
        "priority": None,
        "observationPeriod": None
    }
}

# Query and populate the intent data
intent_uri = rdflib.URIRef("http://example.org/intent/1")

for pred, obj in g.predicate_objects(intent_uri):
    if pred == rdflib.URIRef("http://example.org/intentAdminState"):
        intent_data["intent"]["adminState"] = str(obj)
    elif pred == rdflib.URIRef("http://example.org/intentPriority"):
        intent_data["intent"]["priority"] = int(obj)
    elif pred == rdflib.URIRef("http://example.org/observationPeriod"):
        intent_data["intent"]["observationPeriod"] = int(obj)
    elif pred == rdflib.URIRef("http://example.org/userLabel"):
        intent_data["intent"]["userLabel"] = str(obj)
    elif pred == rdflib.URIRef("http://example.org/intentContext"):
        context = {}
        for p, o in g.predicate_objects(obj):
            if p == rdflib.URIRef("http://example.org/contextAttribute"):
                context["contextAttribute"] = str(o)
            elif p == rdflib.URIRef("http://example.org/contextCondition"):
                context["contextCondition"] = str(o)
            elif p == rdflib.URIRef("http://example.org/contextValueRange"):
                context["contextValueRange"] = str(o)
        intent_data["intent"]["intentContexts"].append(context)
    elif pred == rdflib.URIRef("http://example.org/intentExpectation"):
        expectation = {"expectationContexts": [], "expectationTargets": []}
        for p, o in g.predicate_objects(obj):
            if p == rdflib.URIRef("http://example.org/expectationVerb"):
                expectation["verb"] = str(o)
            elif p == rdflib.URIRef("http://example.org/objectInstance"):
                expectation["objectInstance"] = str(o)
            elif p == rdflib.URIRef("http://example.org/objectType"):
                expectation["objectType"] = str(o)
            elif p == rdflib.URIRef("http://example.org/intentContext"):
                context = {}
                for cp, co in g.predicate_objects(o):
                    if cp == rdflib.URIRef("http://example.org/contextAttribute"):
                        context["contextAttribute"] = str(co)
                    elif cp == rdflib.URIRef("http://example.org/contextCondition"):
                        context["contextCondition"] = str(co)
                    elif cp == rdflib.URIRef("http://example.org/contextValueRange"):
                        context["contextValueRange"] = str(co)
                expectation["expectationContexts"].append(context)
        intent_data["intent"]["intentExpectations"].append(expectation)

# Query and populate the target data
for expectation in intent_data["intent"]["intentExpectations"]:
    for target in g.objects(intent_uri, rdflib.URIRef("http://example.org/intentTarget")):
        target_data = {}
        for p, o in g.predicate_objects(target):
            if p == rdflib.URIRef("http://example.org/targetName"):
                target_data["targetName"] = str(o)
            elif p == rdflib.URIRef("http://example.org/targetCondition"):
                target_data["targetCondition"] = str(o)
            elif p == rdflib.URIRef("http://example.org/targetValueRange"):
                target_data["targetValueRange"] = str(o)
            elif p == rdflib.URIRef("http://example.org/targetContext"):
                context = {}
                for cp, co in g.predicate_objects(o):
                    if cp == rdflib.URIRef("http://example.org/contextAttribute"):
                        context["contextAttribute"] = str(co)
                    elif cp == rdflib.URIRef("http://example.org/contextCondition"):
                        context["contextCondition"] = str(co)
                    elif cp == rdflib.URIRef("http://example.org/contextValueRange"):
                        context["contextValueRange"] = str(co)
                target_data["targetContext"] = context
        expectation["expectationTargets"].append(target_data)

# Convert the intent data to YAML
yaml_data = yaml.dump(intent_data, default_flow_style=False)

# Print the YAML data
print(yaml_data)
