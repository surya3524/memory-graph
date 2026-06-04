"""
Streamlit Advisor Dashboard — Client Financial Memory Graph
Run with: streamlit run dashboard.py
"""

import streamlit as st
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime, timezone

from graph_engine import build_graph, get_client_subgraph, get_client_timeline, graph_summary
from trigger import MARKET_SCENARIOS, run_trigger, ACTION_COLORS
from sample_clients import CLIENTS

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Client Memory Graph",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Styles ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  .main { background-color: #F5F7FA; }
  .stTabs [data-baseweb="tab"] { font-size: 15px; font-weight: 600; }
  .alert-card {
    background: white;
    border-left: 5px solid #C8A034;
    padding: 16px 20px;
    border-radius: 6px;
    margin-bottom: 14px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  }
  .client-card {
    background: white;
    padding: 14px 18px;
    border-radius: 6px;
    margin-bottom: 10px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  }
  .node-chip {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
    margin: 2px;
    color: white;
  }
  h1, h2, h3 { color: #003087; }
</style>
""", unsafe_allow_html=True)

NODE_COLORS = {
    "client":  "#003087",
    "belief":  "#7C3AED",
    "emotion": "#B45309",
    "action":  "#991B1B",
    "event":   "#065F46",
}

ACTION_BADGE = {
    "CALL FIRST":               ("🔴", "#CC2200"),
    "CALL THIS WEEK":           ("🟠", "#E05C00"),
    "CALL CAROL FIRST, THEN JIM": ("🟠", "#E05C00"),
    "EMAIL TODAY":              ("🟡", "#B45309"),
    "PROACTIVE EMAIL":          ("🟡", "#B45309"),
    "PROACTIVE EXPLANATION — EMAIL BEFORE SHE SENDS ONE": ("🟡", "#B45309"),
    "HEADS UP":                 ("🟢", "#1A7A3A"),
    "GENTLE CHECK-IN":          ("🟢", "#1A7A3A"),
    "MONITOR":                  ("🟢", "#1A7A3A"),
}

@st.cache_resource
def load_graph():
    return build_graph()

G = load_graph()
summary = graph_summary(G)
client_lookup = {c["id"]: c for c in CLIENTS}

# ── Sidebar ───────────────────────────────────────────────────────────────────
VERSION = "v0.1.0"
DEPLOYED = "2026-06-03"

with st.sidebar:
    st.markdown(
        "<div style='background:#003087;padding:14px 16px;border-radius:8px;margin-bottom:8px'>"
        "<span style='color:#C8A034;font-size:20px;font-weight:800;letter-spacing:1px'>RAYMOND JAMES</span><br>"
        "<span style='color:#FFFFFF;font-size:11px;letter-spacing:2px'>FINANCIAL SERVICES</span>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("## Client Memory Graph")
    st.caption("Advisor Intelligence POC · RJ Engineering Challenge 2026")
    st.markdown(
        f"<span style='font-size:11px;color:#94A3B8'>{VERSION} &nbsp;·&nbsp; Deployed {DEPLOYED}</span>",
        unsafe_allow_html=True,
    )
    st.divider()

    col1, col2, col3 = st.columns(3)
    col1.metric("Clients", summary["clients"])
    col2.metric("Nodes", summary["total_nodes"])
    col3.metric("Edges", summary["total_edges"])
    st.divider()

    st.markdown("**Select Client**")
    client_options = {c["name"]: c["id"] for c in CLIENTS}
    selected_name = st.selectbox("", list(client_options.keys()), label_visibility="collapsed")
    selected_id   = client_options[selected_name]
    selected_data = client_lookup[selected_id]

    st.divider()
    st.caption("Node types")
    for kind, color in NODE_COLORS.items():
        st.markdown(
            f'<span class="node-chip" style="background:{color}">{kind}</span>',
            unsafe_allow_html=True,
        )

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "⚡  Market Alerts",
    "🧠  Client Memory Graph",
    "📅  Memory Timeline",
    "✍️  Note Encoder",
])

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 1 — Market Alerts
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab1:
    st.markdown("## Market Event → Advisor Action")
    st.caption("Select a market scenario and see which clients need attention, why, and what to say.")

    scenario_labels = {v["label"]: k for k, v in MARKET_SCENARIOS.items()}
    chosen_label = st.selectbox(
        "Select a market scenario",
        list(scenario_labels.keys()),
    )
    chosen_key = scenario_labels[chosen_label]
    scenario   = MARKET_SCENARIOS[chosen_key]

    st.info(f"**{scenario['label']}** — {scenario['description']}")

    alerts = run_trigger(chosen_key)

    if not alerts:
        st.success("No clients flagged for this trigger. No action needed today.")
    else:
        st.markdown(f"### {len(alerts)} client(s) need your attention")
        for a in alerts:
            action = a["alert"]["action"]
            icon, color = ACTION_BADGE.get(action, ("⚪", "#888"))
            st.markdown(f"""
            <div class="alert-card" style="border-left-color:{color}">
              <div style="display:flex;justify-content:space-between;align-items:center">
                <div>
                  <span style="font-size:22px;font-weight:700;color:#003087">{a['name']}</span>
                  &nbsp;
                  <span style="background:{color};color:white;padding:3px 12px;
                        border-radius:12px;font-size:12px;font-weight:700">
                    {icon} {action}
                  </span>
                </div>
                <span style="color:#64748B;font-size:13px">{a['archetype']}</span>
              </div>
              <hr style="margin:10px 0;border-color:#eee">
              <p style="color:#1A1A2E;margin:4px 0"><strong>Why now:</strong><br>{a['alert']['context']}</p>
              <p style="color:#003087;margin:8px 0"><strong>Suggested approach:</strong><br>{a['alert']['suggested_approach']}</p>
              <p style="color:#888;font-size:12px;margin:4px 0">
                Trigger conditions: {' · '.join(a['trigger_conditions'])}
              </p>
            </div>
            """, unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 2 — Client Memory Graph
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab2:
    st.markdown(f"## {selected_name} — Memory Graph")
    st.caption(f"Archetype: {selected_data['archetype']}")

    sub = get_client_subgraph(G, selected_id)

    fig, ax = plt.subplots(figsize=(14, 7))
    ax.set_facecolor("#F5F7FA")
    fig.patch.set_facecolor("#F5F7FA")

    pos = nx.spring_layout(sub, seed=42, k=2.5)

    node_colors = [
        NODE_COLORS.get(sub.nodes[n].get("kind", "belief"), "#888")
        for n in sub.nodes()
    ]
    node_sizes = [
        1800 if sub.nodes[n].get("kind") == "client" else 900
        for n in sub.nodes()
    ]

    nx.draw_networkx_nodes(sub, pos, ax=ax,
        node_color=node_colors, node_size=node_sizes, alpha=0.92)

    nx.draw_networkx_edges(sub, pos, ax=ax,
        edge_color="#C8A034", arrows=True,
        arrowsize=18, width=1.5, alpha=0.7,
        connectionstyle="arc3,rad=0.08")

    labels = {}
    for n in sub.nodes():
        d = sub.nodes[n]
        if d.get("kind") == "client":
            labels[n] = d.get("name", n)
        else:
            raw = d.get("label", n.split("__")[-1])
            labels[n] = raw.replace("_", "\n")

    nx.draw_networkx_labels(sub, pos, labels=labels, ax=ax,
        font_size=7, font_color="white", font_weight="bold")

    edge_labels = {(u, v): d.get("relation", "")
                   for u, v, d in sub.edges(data=True) if d.get("relation") != "HAS"}
    nx.draw_networkx_edge_labels(sub, pos, edge_labels=edge_labels, ax=ax,
        font_size=6.5, font_color="#64748B",
        bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.7))

    legend = [mpatches.Patch(color=c, label=k) for k, c in NODE_COLORS.items()]
    ax.legend(handles=legend, loc="lower left", fontsize=9,
              framealpha=0.9, edgecolor="#ddd")
    ax.axis("off")
    ax.set_title(f"{selected_name} — Belief & Event Memory Graph",
                 fontsize=14, color="#003087", fontweight="bold", pad=15)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.divider()
    st.markdown("**Graph statistics for this client**")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total nodes", sub.number_of_nodes())
    c2.metric("Total edges", sub.number_of_edges())
    c3.metric("Meetings logged", len(selected_data["meetings"]))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 3 — Memory Timeline
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab3:
    st.markdown(f"## {selected_name} — Memory Timeline")
    st.caption("How this client's beliefs, actions, and emotions have evolved over time.")

    for meeting in selected_data["meetings"]:
        date  = meeting["date"]
        nodes = meeting["nodes"]
        note  = meeting["note"]

        st.markdown(f"#### 📅 {date}")
        st.markdown(f"""
        <div class="client-card">
          <p style="color:#1A1A2E;font-style:italic;margin-bottom:10px">"{note}"</p>
          <div>
        """, unsafe_allow_html=True)

        chips = ""
        for n in nodes:
            color = NODE_COLORS.get(n["type"], "#888")
            chips += f'<span class="node-chip" style="background:{color}">{n["label"].replace("_"," ")}</span>'

        st.markdown(chips + "</div></div>", unsafe_allow_html=True)

    st.divider()
    st.markdown("**Advisor Alert Summary**")
    alert = selected_data["advisor_alert"]
    action = alert["action"]
    icon, color = ACTION_BADGE.get(action, ("⚪", "#888"))

    st.markdown(f"""
    <div class="alert-card" style="border-left-color:{color}">
      <p><strong>Trigger:</strong> {alert['trigger']}</p>
      <p><span style="background:{color};color:white;padding:3px 12px;
            border-radius:12px;font-size:12px;font-weight:700">{icon} {action}</span></p>
      <p><strong>Context:</strong> {alert['context']}</p>
      <p><strong>Suggested approach:</strong> {alert['suggested_approach']}</p>
    </div>
    """, unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 4 — Note Encoder
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab4:
    st.markdown("## Meeting Note → Memory Graph")
    st.caption("Paste raw advisor notes. Claude extracts the belief nodes, edges, and advisor alert automatically.")

    col_a, col_b = st.columns([1, 1])

    with col_a:
        note_client = st.selectbox("Client", list(client_options.keys()), key="enc_client")
        note_date   = st.date_input("Meeting date", value=datetime.today())
        note_text   = st.text_area(
            "Paste meeting notes here",
            height=220,
            placeholder=(
                "e.g. Client called today concerned about the market. "
                "Said he's thinking about moving to cash. "
                "Referenced his 2020 experience and said he regretted selling then..."
            ),
        )
        run_btn = st.button("Extract Memory Nodes", type="primary", use_container_width=True)

    with col_b:
        if run_btn and note_text.strip():
            import os
            if not os.environ.get("ANTHROPIC_API_KEY"):
                st.error("Set the ANTHROPIC_API_KEY environment variable to use the encoder.")
            else:
                with st.spinner("Reading notes and building graph nodes..."):
                    from encoder import encode_meeting_note
                    result = encode_meeting_note(
                        note_client,
                        str(note_date),
                        note_text,
                    )

                st.success("Nodes extracted successfully")

                st.markdown("**Nodes**")
                for n in result.get("nodes", []):
                    color = NODE_COLORS.get(n["type"], "#888")
                    st.markdown(
                        f'<span class="node-chip" style="background:{color}">'
                        f'{n["type"].upper()}</span> '
                        f'**{n["label"].replace("_"," ")}** — {n["summary"]}',
                        unsafe_allow_html=True,
                    )

                st.markdown("**Edges**")
                for e in result.get("edges", []):
                    st.markdown(
                        f'`{e["from"]}` → **{e["relation"]}** → `{e["to"]}`'
                    )

                alert = result.get("advisor_alert", {})
                if alert:
                    action = alert.get("action", "")
                    icon, color = ACTION_BADGE.get(action, ("⚪", "#888"))
                    st.markdown("**Advisor Alert**")
                    st.markdown(f"""
                    <div class="alert-card" style="border-left-color:{color}">
                      <p><span style="background:{color};color:white;padding:3px 10px;
                            border-radius:12px;font-size:12px;font-weight:700">
                        {icon} {action}</span></p>
                      <p><strong>Trigger:</strong> {alert.get('trigger','')}</p>
                      <p><strong>Context:</strong> {alert.get('context','')}</p>
                      <p><strong>Approach:</strong> {alert.get('suggested_approach','')}</p>
                    </div>
                    """, unsafe_allow_html=True)
        elif run_btn:
            st.warning("Please paste some meeting notes first.")
        else:
            st.info("Enter meeting notes on the left and click **Extract Memory Nodes**.")
            st.markdown("**How it works:**")
            st.markdown("""
            1. You paste raw advisor notes (free text, however you write them)
            2. Claude reads the notes and identifies what the client *said*, *felt*, and *did*
            3. Those become structured nodes in the memory graph
            4. The system generates an advisor alert for future market events
            5. Nothing is inferred — only what the client explicitly stated is encoded
            """)
