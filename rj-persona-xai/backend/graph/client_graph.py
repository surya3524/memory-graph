import networkx as nx
from graph.sample_data import CLIENT_GRAPHS

def load_client_graph(client_id: str) -> nx.DiGraph:
    data = CLIENT_GRAPHS.get(client_id)
    if not data:
        raise ValueError(f"Client {client_id} not found")
    G = nx.DiGraph()
    for node in data["nodes"]:
        G.add_node(node["node_id"], **node)
    for edge in data["edges"]:
        G.add_edge(edge["source"], edge["target"], **edge)
    return G

def get_context_for_prompt(client_id: str, max_nodes: int = 4) -> dict:
    data = CLIENT_GRAPHS[client_id]
    sorted_nodes = sorted(data["nodes"], key=lambda n: n["weight"], reverse=True)
    top_nodes = sorted_nodes[:max_nodes]

    lines = []
    for n in top_nodes:
        t = n["node_type"].upper()
        label = n["label"]
        val = n["value"]
        if isinstance(val, dict):
            val_str = ", ".join(f"{k}: {v}" for k, v in val.items())
        else:
            val_str = str(val)
        lines.append(f"[{t}] {label} — {val_str}")

    key_signals = [n["label"] for n in top_nodes]

    return {
        "context_text": "\n".join(lines),
        "nodes_used": top_nodes,
        "key_signals": key_signals
    }

def get_graph_for_viz(client_id: str) -> dict:
    data = CLIENT_GRAPHS[client_id]
    return {
        "nodes": [
            {
                "id": n["node_id"],
                "label": n["label"],
                "type": n["node_type"],
                "weight": n["weight"]
            }
            for n in data["nodes"]
        ],
        "edges": [
            {
                "source": e["source"],
                "target": e["target"],
                "relationship": e["relationship"],
                "strength": e["strength"]
            }
            for e in data["edges"]
        ]
    }
