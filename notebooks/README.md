# Notebooks

Notebooks demonstrating the planning ontology. Each notebook
opens in Google Colab and its first cell installs dependencies and fetches the
sample data, so no local setup is required.

Within each notebook, a **Core** path covers the essentials. Optional **Go
deeper** cells add advanced material: writing your own SPARQL, extending the
ontology, or running a planner.

## Notebooks

- `00_quickstart.ipynb`: **Quickstart.** Load the prebuilt KG and answer a
  planner-selection question and an explanation question through helper
  functions, with no SPARQL required. A fast first win for newcomers.
- `01_ontology_and_kg.ipynb`: **Foundations.** Load the ontology from the PURL
  (`https://purl.org/ai4s/ontology/planning`) with RDFLib, explore the schema
  (`PlanningDomain`, `Planner`, `Plan`, `Action`, `Step`) and competency
  questions, ingest a PDDL domain and problem to populate a knowledge graph, and
  run sample SPARQL queries.
- `02_planner_selection.ipynb`: **Use case 1.** Rank planners for a domain via
  SPARQL over a prebuilt IPC KG. As an option, run a PDDL planner and write fresh
  results back into the KG.
- `03_plan_explanation.ipynb`: **Use case 2.** Retrieve a plan's ordered steps
  and their `hasActionExplanation` values and assemble a template-based,
  human-readable narrative.

Each notebook carries optional **Go deeper** visuals and reasoning: a
schema diagram, an RDFS reasoning step, an interactive graph view (01), a
relevance heatmap and portfolio chart (02), and a plan-state diagram with
causal links (03). These need the `viz` extra (`matplotlib`, `pyvis`,
`networkx`, `owlrl`); the Core path needs only `rdflib` and `pandas`.

## Colab convention

The first cell of each notebook installs the core dependencies and fetches the
data:

```python
!pip install -q rdflib pandas
!git clone -q https://github.com/ai4society/ICAPS26-planning-ontology-tutorial.git
%cd ICAPS26-planning-ontology-tutorial
```

The planner-selection notebook adds `unified-planning up-pyperplan` for its
optional live-run section. Unified Planning is a third-party library.

Add an **Open in Colab** badge at the top of each notebook pointing to
`https://colab.research.google.com/github/ai4society/ICAPS26-planning-ontology-tutorial/blob/main/notebooks/<name>.ipynb`.
