"""
Graph Engine — builds and queries the client memory graph using NetworkX.
"""

import json
import networkx as nx
from datetime import datetime
from sample_clients import CLIENTS


def build_graph() -> nx.DiGraph:
    G = nx.DiGraph()

    for client in CLIENTS:
        cid = client["id"]

        G.add_node(cid,
            kind="client",
            name=client["name"],
            age=client["age"],
            archetype=client["archetype"],
            alert_priority=client["alert_priority"],
            trigger_conditions=client["trigger_conditions"],
            advisor_alert=client["advisor_alert"],
        )

        for meeting in client["meetings"]:
            date = meeting["date"]

            for node in meeting["nodes"]:
                node_id = f"{cid}__{node['label']}"
                G.add_node(node_id,
                    kind=node["type"],
                    label=node["label"],
                    date=date,
                    client_id=cid,
                )
                G.add_edge(cid, node_id,
                    relation="HAS",
                    date=date,
                )

            for (src_label, relation, tgt_label) in meeting["edges"]:
                src_id = f"{cid}__{src_label}"
                tgt_id = f"{cid}__{tgt_label}"
                if G.has_node(src_id) and G.has_node(tgt_id):
                    G.add_edge(src_id, tgt_id,
                        relation=relation,
                        date=date,
                    )

    return G


def get_client_subgraph(G: nx.DiGraph, client_id: str) -> nx.DiGraph:
    nodes = [n for n, d in G.nodes(data=True)
             if n == client_id or d.get("client_id") == client_id]
    return G.subgraph(nodes).copy()


def get_client_timeline(G: nx.DiGraph, client_id: str) -> list:
    nodes = [
        (n, d) for n, d in G.nodes(data=True)
        if d.get("client_id") == client_id
    ]
    nodes.sort(key=lambda x: x[1].get("date", ""))
    return nodes


def query_alerts(G: nx.DiGraph, trigger: str) -> list:
    """
    Given a trigger keyword, return ranked list of clients who match it,
    with their advisor alert context.
    """
    results = []
    for n, d in G.nodes(data=True):
        if d.get("kind") != "client":
            continue
        conditions = d.get("trigger_conditions", [])
        if any(trigger.lower() in c.lower() for c in conditions):
            results.append({
                "client_id": n,
                "name": d["name"],
                "archetype": d["archetype"],
                "priority": d["alert_priority"],
                "alert": d["advisor_alert"],
                "trigger_conditions": conditions,
            })
    results.sort(key=lambda x: x["priority"])
    return results


def graph_summary(G: nx.DiGraph) -> dict:
    clients = [n for n, d in G.nodes(data=True) if d.get("kind") == "client"]
    return {
        "total_nodes": G.number_of_nodes(),
        "total_edges": G.number_of_edges(),
        "clients": len(clients),
        "node_kinds": {
            k: sum(1 for _, d in G.nodes(data=True) if d.get("kind") == k)
            for k in ["client", "belief", "emotion", "action", "event"]
        },
    }


if __name__ == "__main__":
    G = build_graph()
    summary = graph_summary(G)
    print("Graph built successfully\n")
    print(f"  Total nodes : {summary['total_nodes']}")
    print(f"  Total edges : {summary['total_edges']}")
    print(f"  Clients     : {summary['clients']}")
    print(f"  Node breakdown: {summary['node_kinds']}\n")

    print("Sample alert query — trigger: 'market_drop_5pct'")
    alerts = query_alerts(G, "market_drop_5pct")
    for a in alerts:
        print(f"  [{a['alert']['action']}] {a['name']} — {a['archetype']}")
