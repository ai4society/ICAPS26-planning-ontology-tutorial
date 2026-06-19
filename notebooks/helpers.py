"""Helper functions for the ICAPS 2026 Planning Ontology Tutorial.

These wrap the SPARQL queries from notebooks 02 and 03 so the Quickstart can answer
planner-selection and plan-explanation questions in one line each. Open those
notebooks to see the queries these functions run.
"""
from pathlib import Path

from rdflib import Graph, Literal, Namespace

PO = Namespace("https://purl.org/ai4s/ontology/planning#")
TUT = Namespace("https://w3id.org/planning-ontology-tutorial#")

PREFIX = (
    "PREFIX po: <https://purl.org/ai4s/ontology/planning#> "
    "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> "
    "PREFIX tut: <https://w3id.org/planning-ontology-tutorial#> "
)


def load_kg(data_dir, name="blocksworld_tutorial.ttl"):
    """Load a prebuilt tutorial knowledge graph from the data directory."""
    graph = Graph()
    graph.parse(str(Path(data_dir) / "kgs" / name), format="turtle")
    return graph


def rank_planners(graph, domain="blocksworld"):
    """Return [(relevance, planner), ...] for a domain, high relevance first."""
    query = PREFIX + """
    SELECT ?relevance ?planner WHERE {
      VALUES (?prop ?relevance ?order) {
        (po:hasHighRelevancePlanner   "high"   1)
        (po:hasMediumRelevancePlanner "medium" 2)
        (po:hasLowRelevancePlanner    "low"    3)
      }
      ?d rdfs:label ?domain .
      ?d ?prop ?p .
      ?p rdfs:label ?planner .
    } ORDER BY ?order ?planner
    """
    return [(str(r.relevance), str(r.planner))
            for r in graph.query(query, initBindings={"domain": Literal(domain)})]


def recommend_planner(graph, domain="blocksworld"):
    """Return the single recommended planner label for a domain, or None."""
    query = PREFIX + """
    SELECT ?planner WHERE {
      ?d rdfs:label ?domain .
      OPTIONAL { ?d po:hasHighRelevancePlanner   ?h . ?h rdfs:label ?hl }
      OPTIONAL { ?d po:hasMediumRelevancePlanner ?m . ?m rdfs:label ?ml }
      OPTIONAL { ?d po:hasLowRelevancePlanner    ?l . ?l rdfs:label ?ll }
      BIND(COALESCE(?hl, ?ml, ?ll) AS ?planner)
    } ORDER BY ?planner LIMIT 1
    """
    rows = [str(r.planner)
            for r in graph.query(query, initBindings={"domain": Literal(domain)})]
    return rows[0] if rows else None


def plan_story(graph, problem="problem_3_1"):
    """Return the plan-level explanation text for a problem, or None."""
    query = PREFIX + """
    SELECT ?explanation WHERE {
      ?prob rdfs:label ?problem .
      ?prob po:hasPlan ?plan .
      ?plan po:hasPlanExplanation ?explanation .
    }
    """
    rows = [str(r.explanation)
            for r in graph.query(query, initBindings={"problem": Literal(problem)})]
    return rows[0] if rows else None


def _parameters_in_order(graph, action_iri):
    query = PREFIX + """
    SELECT ?plabel WHERE { ?act po:hasParameter ?p . ?p rdfs:label ?plabel }
    ORDER BY ?p
    """
    return [str(r.plabel).split()[0]
            for r in graph.query(query, initBindings={"act": action_iri})]


def explain_plan(graph, problem="problem_3_1", grounded=True):
    """Return [(step_number, grounded_action, explanation), ...] in plan order.

    With ``grounded=True`` this fills the action templates with the step's actual
    arguments, so ``?x`` and ``?y`` become the blocks the step acts on.
    """
    query = PREFIX + """
    SELECT ?n ?grounded ?act ?explanation WHERE {
      ?prob rdfs:label ?problem .
      ?prob po:hasPlan ?plan .
      ?step tut:stepOf ?plan ;
            tut:stepNumber ?n ;
            rdfs:label ?grounded ;
            tut:groundsAction ?act .
      ?act po:hasActionExplanation ?explanation .
    } ORDER BY ?n
    """
    steps = []
    for r in graph.query(query, initBindings={"problem": Literal(problem)}):
        text = str(r.explanation)
        if grounded:
            variables = _parameters_in_order(graph, r.act)
            arguments = str(r.grounded).split()[1:]  # drop the action name
            for var, arg in zip(variables, arguments):
                text = text.replace(var, arg)
        steps.append((int(r.n), str(r.grounded), text))
    return steps
