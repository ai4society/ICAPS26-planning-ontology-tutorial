"""Plan-explanation logic for the ICAPS 2026 Planning Ontology Tutorial.

Parses predicate-level action schemas from PDDL, simulates a grounded plan,
and computes causal links so a notebook can explain why a plan is ordered the
way it is. Drawing lives in viz.py; this module stays text only.
"""
from __future__ import annotations

import re

from rdflib import Literal, RDFS


def _sexpr(text):
    """Parse a parenthesized string into nested lists of tokens."""
    tokens = re.findall(r"\(|\)|[^\s()]+", text)
    stack = [[]]
    for tok in tokens:
        if tok == "(":
            new = []
            stack[-1].append(new)
            stack.append(new)
        elif tok == ")":
            stack.pop()
        else:
            stack[-1].append(tok)
    return stack[0]


def _keyed(items):
    """Group [':parameters', val, ':precondition', val, ...] into a dict."""
    out = {}
    i = 0
    while i < len(items) - 1:
        key = items[i]
        if isinstance(key, str) and key.startswith(":"):
            out[key] = items[i + 1]
            i += 2
        else:
            i += 1
    return out


def _flatten_pre(node):
    """Positive precondition atoms as tuples. Blocksworld has no negatives."""
    if not node:
        return []
    if node[0] == "and":
        atoms = []
        for child in node[1:]:
            atoms += _flatten_pre(child)
        return atoms
    if node[0] == "not":
        return []
    return [tuple(node)]


def _split_effects(node):
    """Return (add_atoms, del_atoms) from an effect node."""
    add, dele = [], []
    if not node:
        return add, dele
    children = node[1:] if node and node[0] == "and" else [node]
    for child in children:
        if child and child[0] == "not":
            dele.append(tuple(child[1]))
        else:
            add.append(tuple(child))
    return add, dele


def parse_action_schemas(domain_text):
    """Return {name: {"params", "pre", "add", "del"}} for each PDDL action."""
    define = _sexpr(domain_text)[0]
    schemas = {}
    for node in define:
        if isinstance(node, list) and node and node[0] == ":action":
            name = node[1]
            keyed = _keyed(node[2:])
            params = [t for t in keyed.get(":parameters", [])
                      if isinstance(t, str) and t.startswith("?")]
            pre = _flatten_pre(keyed.get(":precondition"))
            add, dele = _split_effects(keyed.get(":effect"))
            schemas[name] = {"params": params, "pre": pre, "add": add, "del": dele}
    return schemas


def parse_init(problem_text):
    """Return the problem's :init atoms as tuples."""
    define = _sexpr(problem_text)[0]
    for node in define:
        if isinstance(node, list) and node and node[0] == ":init":
            return [tuple(atom) for atom in node[1:] if isinstance(atom, list)]
    return []


def parse_step(step):
    """'stack b2 b1' -> ('stack', ['b2', 'b1'])."""
    name, *args = step.split()
    return name, args


def ground(atom, params, args):
    """Substitute ?vars in a predicate tuple with concrete args."""
    binding = dict(zip(params, args))
    return tuple(binding.get(t, t) for t in atom)


def simulate_states(init, steps, schemas):
    """Replay the plan; return [state_0, ...] of frozensets, state_0 = init."""
    state = {tuple(a) for a in init}
    history = [frozenset(state)]
    for step in steps:
        name, args = parse_step(step)
        sch = schemas[name]
        for d in sch["del"]:
            state.discard(ground(d, sch["params"], args))
        for a in sch["add"]:
            state.add(ground(a, sch["params"], args))
        history.append(frozenset(state))
    return history


def causal_links(init, steps, schemas):
    """For each step, the (producer_index, predicate) pairs supporting its
    preconditions. Producer 0 is the initial state; otherwise the 1-based
    index of the most recent earlier step that adds the predicate.
    """
    producers = {tuple(a): 0 for a in init}
    out = []
    for i, step in enumerate(steps, start=1):
        name, args = parse_step(step)
        sch = schemas[name]
        links = []
        for p in sch["pre"]:
            gp = ground(p, sch["params"], args)
            if gp in producers:
                links.append((producers[gp], gp))
        out.append({"step": i, "action": step, "links": links})
        for d in sch["del"]:
            producers.pop(ground(d, sch["params"], args), None)
        for a in sch["add"]:
            producers[ground(a, sch["params"], args)] = i
    return out


def atom_label(atom):
    """('on','?x','?y') -> 'on(?x, ?y)'."""
    head, *args = atom
    return f"{head}({', '.join(args)})" if args else f"{head}()"


def _atom_id(atom):
    return "_".join(atom).replace("?", "").replace("-", "_")


def schemas_to_triples(graph, schemas, po, tut):
    """Add predicate-level pre/eff for each action under the tut: extension.

    Properties: tut:hasPreconditionPredicate, tut:hasAddEffect, tut:hasDelEffect.
    Each points at a node carrying an rdfs:label such as 'on(?x, ?y)'. Leaves
    the published po: vocabulary untouched. Returns the number of triples added.
    """
    before = len(graph)
    props = {"pre": tut.hasPreconditionPredicate,
             "add": tut.hasAddEffect,
             "del": tut.hasDelEffect}
    for name, sch in schemas.items():
        action = po[name]
        for key, prop in props.items():
            for atom in sch[key]:
                node = tut[f"{name}_{key}_{_atom_id(atom)}"]
                graph.add((node, RDFS.label, Literal(atom_label(atom))))
                graph.add((action, prop, node))
    return len(graph) - before
