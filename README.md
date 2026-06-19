# Planning Ontology Tutorial

### Knowledge Representation and Explainable Planning

**ICAPS 2026 Tutorial**

> You use the planning ontology to turn scattered planning artifacts (PDDL
> domains, problems, plans, and planner benchmarks) into a queryable
> **RDF/OWL knowledge graph**, then exploit that graph for two applications:
> **data-driven planner selection** and **human-readable plan explanations**.

📅 Venue and schedule: _TBD_ · 🔗 Ontology PURL: <https://purl.org/ai4s/ontology/planning>

---

## Overview

Automated planning offers many planners and domains, but the performance data and
domain models sit in static, disconnected files such as IPC reports and PDDL. You
model the core concepts (`PlanningDomain`, `Planner`, `Plan`, `Action`, `Step`)
as OWL classes and properties, populate a knowledge graph from public datasets,
and query it with **SPARQL** as an "ask-me-anything" layer over planning
knowledge.

Two use cases anchor the tutorial:

1. **SPARQL-driven planner selection.** Rank planners for a domain by required
   features and past performance (_"which planner has the highest relevance score
   for the `blocksworld` domain?"_). As an option, run a PDDL planner on a problem
   and add the fresh results to the KG.
2. **Plan explanation extraction.** Query a plan's ordered `Step`s and their
   `hasActionExplanation` values, then compose a human-readable narrative.

## Setup

> [!NOTE]
> For Colab, skip this section. The first cell of each notebook installs what it needs.

To run locally, pick one of the following.

With [uv](https://docs.astral.sh/uv/) (recommended):

```bash
uv sync                   # core packages plus the notebook tooling
uv sync --extra planner   # add the optional PDDL planner used in notebook 02
uv run jupyter lab
```

With pip:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

## Notebooks

Start with the Quickstart, then open the others in any order. Each runs in Google
Colab with no local setup, since the first cell installs dependencies and fetches
the data. Within each notebook, a **Core** path covers the essentials and optional
**Go deeper** cells add advanced material such as writing your own SPARQL or
extending the ontology.

| Notebook                        | What it covers                                                                                                                                                 | Colab                                                                                                                                         | Source                                                                         |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| **Quickstart**                  | Load the prebuilt KG and answer a planner-selection question and an explanation question through helper functions, no SPARQL required                          | [Open](https://colab.research.google.com/github/ai4society/ICAPS26-planning-ontology-tutorial/blob/main/notebooks/00_quickstart.ipynb)        | [`notebooks/00_quickstart.ipynb`](notebooks/00_quickstart.ipynb)               |
| **Ontology and KG foundations** | Load the ontology from the PURL with RDFLib, explore the schema and competency questions, ingest a PDDL domain and problem to populate a KG, run sample SPARQL | [Open](https://colab.research.google.com/github/ai4society/ICAPS26-planning-ontology-tutorial/blob/main/notebooks/01_ontology_and_kg.ipynb)   | [`notebooks/01_ontology_and_kg.ipynb`](notebooks/01_ontology_and_kg.ipynb)     |
| **Planner selection**           | Rank planners for `blocksworld` via SPARQL over a prebuilt IPC KG. As an option, run a PDDL planner and write fresh results back into the KG                   | [Open](https://colab.research.google.com/github/ai4society/ICAPS26-planning-ontology-tutorial/blob/main/notebooks/02_planner_selection.ipynb) | [`notebooks/02_planner_selection.ipynb`](notebooks/02_planner_selection.ipynb) |
| **Plan explanation**            | Retrieve a plan's ordered steps and their explanations from the KG and assemble a template-based narrative                                                     | [Open](https://colab.research.google.com/github/ai4society/ICAPS26-planning-ontology-tutorial/blob/main/notebooks/03_plan_explanation.ipynb)  | [`notebooks/03_plan_explanation.ipynb`](notebooks/03_plan_explanation.ipynb)   |

> **Status:** all four notebooks are built and runnable. We add the advertising
> website (`website/`) later.

## Resources

- **Planning ontology (PURL):** <https://purl.org/ai4s/ontology/planning>
- **Ontology source and datasets:** <https://github.com/ai4society/planning-ontology>
- **Paper (Discover Data, 2025):** <https://link.springer.com/article/10.1007/s44248-025-00093-9>

## Citation

If you use the planning ontology, please cite the Discover Data paper:

```bibtex
@article{muppasani2025planning,
  title   = {Building a planning ontology to represent and exploit planning knowledge and its applications},
  author  = {Muppasani, Bharath and Gupta, Nitin and Pallagani, Vishal and Srivastava, Biplav and Mutharaju, Raghava and Huhns, Michael N. and Narayanan, Vignesh},
  journal = {Discover Data},
  year    = {2025},
  doi     = {10.1007/s44248-025-00093-9}
}
```

## License

This tutorial uses the [Apache License 2.0](LICENSE).
