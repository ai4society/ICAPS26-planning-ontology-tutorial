"""Build a compact IPC-2018 planner-relevance slice for notebook 02.

Loads the full IPC-2018 instance graph and writes the N domains with the most
planner annotations to a Turtle file in the old ontology namespace, matching
the existing two-domain sample.

Run once:  python scripts/build_ipc_slice.py --domains 10
"""
from __future__ import annotations

import argparse
from pathlib import Path

from rdflib import Graph, Literal, Namespace, RDFS

OLD = Namespace("http://www.semanticweb.org/muppa/ontologies/2022/4/plan-ontology#")
FULL_URL = ("https://raw.githubusercontent.com/ai4society/planning-ontology/main/"
            "AI-Planning-Ontology/models/"
            "plan-ontology-rdf-instances-planner-info_ipc2018.owl")
PROPS = [OLD.hasHighRelevancePlanner,
         OLD.hasMediumRelevancePlanner,
         OLD.hasLowRelevancePlanner]


def _ensure_label(out, subject):
    """Give a subject an rdfs:label from its IRI local name when it has none.

    Some real IPC-2018 domains carry no rdfs:label in the source. A label-based
    query would then drop them, so fall back to the IRI local name and keep the
    slice self-consistent.
    """
    if out.value(subject, RDFS.label) is None:
        local = str(subject).split("#")[-1].split("/")[-1]
        out.add((subject, RDFS.label, Literal(local)))


def build_slice(full, n_domains):
    """Return a Graph holding the n_domains most-annotated domains.

    Every domain and planner is guaranteed an rdfs:label: the source label when
    present, otherwise the IRI local name.
    """
    counts = {}
    for prop in PROPS:
        for d, _ in full.subject_objects(prop):
            counts[d] = counts.get(d, 0) + 1
    chosen = [d for d, _ in sorted(counts.items(),
                                   key=lambda kv: (-kv[1], str(kv[0])))[:n_domains]]
    out = Graph()
    out.bind("po-old", OLD)
    out.bind("rdfs", RDFS)
    planners = set()
    for d in chosen:
        for lbl in full.objects(d, RDFS.label):
            out.add((d, RDFS.label, lbl))
        for prop in PROPS:
            for p in full.objects(d, prop):
                out.add((d, prop, p))
                planners.add(p)
        _ensure_label(out, d)
    for p in planners:
        for lbl in full.objects(p, RDFS.label):
            out.add((p, RDFS.label, lbl))
        _ensure_label(out, p)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domains", type=int, default=10)
    ap.add_argument("--out",
                    default="data/kgs/ipc2018_planner_info_10domains.ttl")
    ap.add_argument("--source", default=FULL_URL)
    args = ap.parse_args()
    full = Graph()
    print(f"loading {args.source} ...")
    full.parse(args.source, format="xml")
    print(f"full graph: {len(full)} triples")
    out = build_slice(full, args.domains)
    Path(args.out).write_text(out.serialize(format="turtle"), encoding="utf-8")
    n = len(set(out.subjects(OLD.hasHighRelevancePlanner)) |
            set(out.subjects(OLD.hasMediumRelevancePlanner)) |
            set(out.subjects(OLD.hasLowRelevancePlanner)))
    print(f"wrote {args.out}: {len(out)} triples, {n} domains")


if __name__ == "__main__":
    main()
