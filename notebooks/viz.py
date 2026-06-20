"""Drawing helpers for the ICAPS 2026 Planning Ontology Tutorial.

Kept out of the Core path. Notebooks import these only inside Go-deeper cells
and install matplotlib/pyvis/networkx/owlrl on demand in Colab. The module does
not force a matplotlib backend, so it renders inline under the notebook kernel.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import networkx as nx
from rdflib import BNode, RDF, RDFS, URIRef
from rdflib.namespace import OWL


def _towers(state):
    """Return (columns, held) where columns is a list of bottom-up block lists."""
    on = {x: y for t in state if t[0] == "on" for x, y in [(t[1], t[2])]}
    above = {y: x for x, y in on.items()}
    ontable = sorted(t[1] for t in state if t[0] == "ontable")
    held = [t[1] for t in state if t[0] == "holding"]
    columns = []
    for base in ontable:
        tower, cur = [base], base
        while cur in above:
            cur = above[cur]
            tower.append(cur)
        columns.append(tower)
    return columns, held


def _block(ax, col, level, label, held=False):
    color = "#ffd9a8" if held else "#bcd3f0"
    ax.add_patch(Rectangle((col - 0.4, level), 0.8, 0.8,
                           facecolor=color, edgecolor="#3a4a5a"))
    ax.text(col, level + 0.4, label, ha="center", va="center", fontsize=9)


def _draw_state(ax, state, blocks):
    columns, held = _towers(state)
    for col, tower in enumerate(columns):
        for level, b in enumerate(tower):
            _block(ax, col, level, b)
    for k, b in enumerate(held):
        _block(ax, len(columns) + k, len(blocks), b, held=True)
    ax.plot([-0.6, max(len(columns), 1) - 0.4], [0, 0], color="#3a4a5a", lw=1.5)
    ax.set_xlim(-0.8, max(len(columns) + len(held), 1) + 0.2)
    ax.set_ylim(-0.4, len(blocks) + 1.2)
    ax.set_aspect("equal")
    ax.axis("off")


def draw_blocks_states(history, titles=None, blocks=None):
    """Draw blocksworld towers for each state in ``history``.

    ``history`` is a list of state sets of (predicate, *args) tuples, as
    returned by explain.simulate_states. Returns the matplotlib Figure.
    """
    n = len(history)
    if blocks is None:
        blocks = sorted({a for st in history for pred in st for a in pred[1:]})
    fig, axes = plt.subplots(1, n, figsize=(2.4 * n, 3))
    if n == 1:
        axes = [axes]
    for ax, state in zip(axes, history):
        _draw_state(ax, state, blocks)
    if titles:
        for ax, title in zip(axes, titles):
            ax.set_title(title, fontsize=9)
    fig.tight_layout()
    return fig


def draw_plan_states(data_dir, steps, domain="blocksworld"):
    """Parse the PDDL under ``data_dir``, simulate ``steps``, draw the towers."""
    import explain
    dom = (Path(data_dir) / "domains" / domain / "domain.pddl").read_text()
    prob = (Path(data_dir) / "domains" / domain / "problem.pddl").read_text()
    schemas = explain.parse_action_schemas(dom)
    init = explain.parse_init(prob)
    history = explain.simulate_states(init, steps, schemas)
    titles = ["start"] + [f"{i}. {s}" for i, s in enumerate(steps, 1)]
    return draw_blocks_states(history, titles=titles)


_BUCKET = {"high": 3, "medium": 2, "low": 1}


def relevance_heatmap(rows):
    """Draw a domain x planner relevance heatmap.

    ``rows`` is an iterable of (domain, planner, bucket). Returns the Figure.
    """
    rows = list(rows)
    domains = sorted({d for d, _, _ in rows})
    planners = sorted({p for _, p, _ in rows})
    di = {d: i for i, d in enumerate(domains)}
    pi = {p: j for j, p in enumerate(planners)}
    grid = [[0] * len(planners) for _ in domains]
    for d, p, b in rows:
        grid[di[d]][pi[p]] = _BUCKET.get(b, 0)
    fig, ax = plt.subplots(figsize=(0.5 * len(planners) + 3, 0.5 * len(domains) + 2))
    im = ax.imshow(grid, aspect="auto", cmap="YlOrRd", vmin=0, vmax=3)
    ax.set_xticks(range(len(planners)))
    ax.set_xticklabels(planners, rotation=45, fontsize=7)
    ax.set_yticks(range(len(domains)))
    ax.set_yticklabels(domains, fontsize=8)
    cbar = fig.colorbar(im, ax=ax, ticks=[0, 1, 2, 3])
    cbar.ax.set_yticklabels(["none", "low", "medium", "high"])
    fig.tight_layout()
    return fig


def _local(uri):
    return str(uri).split("#")[-1].split("/")[-1]


def draw_schema(onto, po):
    """Draw the ontology schema: subClassOf hierarchy plus object properties.

    Skips anonymous (blank-node) restriction classes. Returns the Figure.
    """
    graph = nx.DiGraph()
    edge_labels = {}
    for s, o in onto.subject_objects(RDFS.subClassOf):
        if isinstance(s, BNode) or isinstance(o, BNode):
            continue
        graph.add_edge(_local(s), _local(o), kind="is-a")
    for prop in onto.subjects(RDF.type, OWL.ObjectProperty):
        if not str(prop).startswith(str(po)):
            continue
        domains = [d for d in onto.objects(prop, RDFS.domain)
                   if not isinstance(d, BNode)]
        ranges = [r for r in onto.objects(prop, RDFS.range)
                  if not isinstance(r, BNode)]
        for d in domains:
            for r in ranges:
                graph.add_edge(_local(d), _local(r), kind="prop")
                edge_labels[(_local(d), _local(r))] = _local(prop)
    fig, ax = plt.subplots(figsize=(12, 8))
    pos = nx.spring_layout(graph, seed=7, k=0.9)
    isa = [(u, v) for u, v, d in graph.edges(data=True) if d["kind"] == "is-a"]
    prop = [(u, v) for u, v, d in graph.edges(data=True) if d["kind"] == "prop"]
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_color="#dde7f5", node_size=1600)
    nx.draw_networkx_labels(graph, pos, ax=ax, font_size=7)
    nx.draw_networkx_edges(graph, pos, edgelist=isa, ax=ax, edge_color="#444",
                           style="dashed", arrows=True, node_size=1600)
    nx.draw_networkx_edges(graph, pos, edgelist=prop, ax=ax, edge_color="#2a8a55",
                           arrows=True, node_size=1600)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels,
                                 font_size=6, ax=ax)
    ax.set_title("Planning ontology: dashed = subclass, solid = object property",
                 fontsize=9)
    ax.set_axis_off()
    fig.tight_layout()
    return fig


def kg_to_pyvis(graph, height="500px"):
    """Render an RDF graph as an interactive pyvis Network. Skips literal
    objects and rdf:type/rdfs:label edges; labels nodes by rdfs:label.
    """
    from pyvis.network import Network
    labels = {s: str(o) for s, o in graph.subject_objects(RDFS.label)}
    # "remote" pulls vis-network from a CDN at render time instead of inlining
    # ~600 KB of library into every notebook; Colab and Jupyter both have network.
    net = Network(height=height, width="100%", directed=True,
                  cdn_resources="remote")
    net.barnes_hut()
    added = set()
    for s, p, o in graph:
        if not isinstance(o, URIRef) or p in (RDF.type, RDFS.label):
            continue
        for node in (s, o):
            if node not in added:
                net.add_node(str(node), label=labels.get(node, _local(node)))
                added.add(node)
        net.add_edge(str(s), str(o), label=_local(p))
    return net


def pyvis_html(net):
    """Return the network's HTML for inline display in a notebook."""
    try:
        return net.generate_html(notebook=False)
    except TypeError:
        return net.generate_html()
