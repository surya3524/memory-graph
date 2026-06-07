"""
Streamlit Advisor Dashboard — Client Financial Memory Graph
Run with: streamlit run dashboard.py
"""

import json
import os
import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pyvis.network import Network
from datetime import datetime, timezone

from graph_engine import build_graph, get_client_subgraph, get_client_timeline, graph_summary
from trigger import MARKET_SCENARIOS, run_trigger, ACTION_COLORS
from sample_clients import CLIENTS
from simulation import MARKET_EVENT, SYSTEM_ALERT, PRE_CALL_BRIEF, CONVERSATION, CALL_OUTCOME
from real_conversation import (VOICEMAIL, ADVISOR_PREP, PHONE_CALL, FOLLOW_UP_EMAIL,
                                TEXT_EXCHANGE, THURSDAY_MEETING, NEW_GRAPH_NODES, NEW_GRAPH_EDGES)
from hf_loader import load_hf_clients, HF_RAW_ROWS, HF_RAW_ENCODED

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

def build_pyvis_graph(sub: nx.DiGraph) -> Network:
    net = Network(height="600px", width="100%", directed=True, bgcolor="#F5F7FA")
    net.set_options(json.dumps({
        "physics": {
            "forceAtlas2Based": {
                "gravitationalConstant": -60,
                "centralGravity": 0.005,
                "springLength": 180,
                "springConstant": 0.08,
                "damping": 0.4,
                "avoidOverlap": 0.5,
            },
            "solver": "forceAtlas2Based",
            "stabilization": {"enabled": True, "iterations": 200},
        },
        "edges": {
            "smooth": {"type": "dynamic"},
            "font": {"size": 10, "color": "#44546A", "strokeWidth": 2, "strokeColor": "white"},
        },
        "interaction": {
            "hover": True,
            "tooltipDelay": 80,
            "zoomView": True,
            "dragView": True,
            "navigationButtons": True,
        },
    }))

    for node_id in sub.nodes():
        data   = sub.nodes[node_id]
        kind   = data.get("kind", "belief")
        color  = NODE_COLORS.get(kind, "#888")
        is_hub = kind == "client"
        label  = data.get("name", node_id) if is_hub else data.get("label", node_id.split("__")[-1]).replace("_", " ")

        lines = [f"<b>{label}</b>", f"<i>{kind}</i>"]
        if data.get("date"):
            lines.append(f"📅 {data['date']}")
        if data.get("summary"):
            lines.append(data["summary"])

        net.add_node(
            node_id,
            label=label,
            shape="ellipse",
            size=34 if is_hub else 20,
            color={"background": color, "border": color,
                   "highlight": {"background": color, "border": "#C8A034"}},
            title="<br>".join(lines),
            font={"color": "white", "size": 13 if is_hub else 11, "bold": True},
            widthConstraint={"minimum": 90, "maximum": 130} if is_hub else {"minimum": 70, "maximum": 110},
        )

    for u, v, d in sub.edges(data=True):
        relation = d.get("relation", "")
        is_has   = relation == "HAS"
        net.add_edge(
            u, v,
            label="" if is_has else relation,
            color={"color": "#C8A034", "opacity": 0.35 if is_has else 0.85},
            width=1 if is_has else 2,
            arrows="to",
            font={"size": 9, "color": "#44546A", "strokeWidth": 2, "strokeColor": "white"},
            dashes=is_has,
        )

    return net


@st.cache_resource
def load_graph():
    return build_graph()

G = load_graph()
summary = graph_summary(G)
client_lookup = {c["id"]: c for c in CLIENTS}
hf_clients, hf_live = load_hf_clients(use_live=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
_ver     = json.load(open(os.path.join(os.path.dirname(__file__), "version.json")))
VERSION  = _ver["version"]
DEPLOYED = _ver["deployed"]

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
        f"<span style='font-size:11px;color:#94A3B8'>{VERSION} &nbsp;·&nbsp; Last deployed: {DEPLOYED}</span>",
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

    st.divider()
    st.markdown(
        "<div style='opacity:0.25;font-size:10px'>",
        unsafe_allow_html=True,
    )
    st.checkbox("🔬 dataset", key="hf_mode")
    st.markdown("</div>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
_tab_labels = [
    "⚡  Market Alerts",
    "🧠  Client Memory Graph",
    "📅  Memory Timeline",
    "✍️  Note Encoder",
    "🔴  PHLX Simulation",
    "🎙️  Real Conversation",
]
if st.session_state.get("hf_mode", False):
    _tab_labels.append("🤗  Real Data")

_tabs = st.tabs(_tab_labels)
tab1, tab2, tab3, tab4, tab5, tab6 = _tabs[:6]
tab7 = _tabs[6] if len(_tabs) > 6 else None

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

    net  = build_pyvis_graph(sub)
    html = net.generate_html(notebook=False)
    html = html.replace(
        "network = new vis.Network(container, data, options);",
        "network = new vis.Network(container, data, options);\n"
        "network.once('stabilizationIterationsDone', function() {"
        " network.setOptions({ physics: { enabled: false } }); });",
    )
    components.html(html, height=620, scrolling=False)

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
                "e.g. Client called today with concerns about the market. "
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

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 5 — PHLX Sell-Off Simulation
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab5:
    st.markdown("## PHLX Semiconductor Sell-Off — Live Simulation")
    st.caption("June 3, 2026 · End-to-end workflow: market event → alert → pre-call brief → advisor conversation → new graph nodes")

    # ── Section 1: Market Event ──────────────────────────────────────────────
    st.markdown("### 1  The Market Event")
    ev = MARKET_EVENT
    st.markdown(f"""
    <div style="background:#1A1A2E;border-left:6px solid #CC2200;padding:18px 22px;border-radius:8px;margin-bottom:16px">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <span style="color:#FF4444;font-size:22px;font-weight:800">{ev['index']}</span>
        <span style="color:#FF4444;font-size:32px;font-weight:900">{ev['move']}</span>
      </div>
      <p style="color:#94A3B8;font-size:12px;margin:4px 0">{ev['date']} · {ev['time']}</p>
      <p style="color:#E2E8F0;margin:12px 0 0 0">{ev['catalyst']}</p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(len(ev["movers"]))
    for col, (ticker, move, price) in zip(cols, ev["movers"]):
        col.metric(ticker, price, move)

    st.divider()

    # ── Section 2: System Alert ──────────────────────────────────────────────
    st.markdown("### 2  System Alert — Fired at 09:34 AM EST")
    al = SYSTEM_ALERT
    st.markdown(f"""
    <div class="alert-card" style="border-left-color:#E05C00">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <span style="font-size:20px;font-weight:700;color:#003087">{al['client']}</span>
        <span style="background:#E05C00;color:white;padding:3px 14px;border-radius:12px;font-size:12px;font-weight:700">
          🟠 {al['action']}
        </span>
      </div>
      <p style="color:#64748B;font-size:13px;margin:4px 0">{al['archetype']} · Priority {al['priority']} · Trigger: <code>{al['trigger_matched']}</code></p>
      <hr style="border-color:#eee;margin:10px 0">
      <p style="color:#1A1A2E"><strong>Why now:</strong> {al['context']}</p>
      <p style="color:#003087"><strong>Suggested approach:</strong> {al['suggested_approach']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── Section 3: Pre-Call Brief ────────────────────────────────────────────
    st.markdown("### 3  Advisor Pre-Call Brief")
    st.caption(f"Memory graph reviewed in {PRE_CALL_BRIEF['prep_time']} · {PRE_CALL_BRIEF['graph_nodes_reviewed']} nodes surfaced")

    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.markdown("**Key beliefs to work with**")
        for label, note in PRE_CALL_BRIEF["key_beliefs"]:
            st.markdown(f"""
            <div class="client-card" style="border-left:3px solid #7C3AED;margin-bottom:8px">
              <code style="color:#7C3AED;font-size:11px">{label.replace('_',' ')}</code>
              <p style="margin:4px 0 0 0;font-size:13px;color:#1A1A2E">{note}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("**Key emotions**")
        for label, note in PRE_CALL_BRIEF["key_emotions"]:
            st.markdown(f"""
            <div class="client-card" style="border-left:3px solid #B45309;margin-bottom:8px">
              <code style="color:#B45309;font-size:11px">{label.replace('_',' ')}</code>
              <p style="margin:4px 0 0 0;font-size:13px;color:#1A1A2E">{note}</p>
            </div>
            """, unsafe_allow_html=True)

    with col_b:
        st.markdown("**Household flag**")
        st.markdown(f"""
        <div class="client-card" style="border-left:3px solid #C8A034;background:#FFFBEB">
          <p style="margin:0;font-size:13px;color:#1A1A2E">{PRE_CALL_BRIEF['household_flag']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Open thread from last meeting**")
        st.markdown(f"""
        <div class="client-card" style="border-left:3px solid #003087;background:#EFF6FF">
          <p style="margin:0;font-size:13px;color:#1A1A2E">{PRE_CALL_BRIEF['open_thread']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── Section 4: Conversation ──────────────────────────────────────────────
    st.markdown("### 4  Advisor — Client Conversation")
    st.caption("10:17 AM EST · Phone call · 6 minutes")

    for turn in CONVERSATION:
        is_advisor = turn["speaker"] == "Advisor"
        bg     = "#EFF6FF" if is_advisor else "#F8FAFC"
        border = "#003087" if is_advisor else "#64748B"
        align  = "left"
        label  = f"**Advisor** · {turn['time']}" if is_advisor else f"**Michael T.** · {turn['time']}"

        st.markdown(f"""
        <div style="background:{bg};border-left:4px solid {border};
                    padding:12px 16px;border-radius:6px;margin-bottom:10px">
          <p style="font-size:11px;color:#64748B;margin:0 0 6px 0">{label}</p>
          <p style="margin:0;color:#1A1A2E;font-size:14px">{turn['text']}</p>
        </div>
        """, unsafe_allow_html=True)

        if turn["graph_note"]:
            st.markdown(
                f"<p style='font-size:11px;color:#7C3AED;margin:-6px 0 10px 20px'>"
                f"📍 <em>{turn['graph_note']}</em></p>",
                unsafe_allow_html=True,
            )

    st.divider()

    # ── Section 5: Outcome + New Nodes ──────────────────────────────────────
    st.markdown("### 5  Call Outcome + New Memory Nodes")
    out = CALL_OUTCOME

    res_color = "#065F46" if out["result"] == "SUCCESS" else "#991B1B"
    st.markdown(f"""
    <div class="client-card" style="border-left:5px solid {res_color}">
      <span style="color:{res_color};font-weight:700;font-size:16px">✅ {out['result']}</span>
      &nbsp; <span style="color:#64748B;font-size:13px">{out['duration']}</span>
      <p style="margin:8px 0 0 0;color:#1A1A2E"><strong>Action:</strong> {out['action_taken']}</p>
    </div>
    """, unsafe_allow_html=True)

    col_n, col_e = st.columns([1, 1])
    with col_n:
        st.markdown("**New nodes added to Michael's graph**")
        for n in out["new_nodes"]:
            color = NODE_COLORS.get(n["type"], "#888")
            st.markdown(
                f'<span class="node-chip" style="background:{color}">{n["type"]}</span> '
                f'<code style="font-size:12px">{n["label"].replace("_"," ")}</code> '
                f'<span style="color:#94A3B8;font-size:11px">{n["date"]}</span>',
                unsafe_allow_html=True,
            )
            st.markdown("")

    with col_e:
        st.markdown("**New edges**")
        for src, rel, tgt in out["new_edges"]:
            st.markdown(
                f'<code style="font-size:11px">{src.replace("_"," ")}</code> '
                f'<span style="color:#C8A034;font-weight:700"> → {rel} → </span>'
                f'<code style="font-size:11px">{tgt.replace("_"," ")}</code>',
                unsafe_allow_html=True,
            )
            st.markdown("")

    st.divider()
    st.markdown("**RSI Signal**")
    st.markdown(f"""
    <div class="client-card" style="border-left:4px solid #7C3AED;background:#F5F3FF">
      <p style="margin:0;font-size:13px;color:#1A1A2E">🔁 {out['rsi_signal']}</p>
    </div>
    """, unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 6 — Real Conversation (PHLX Sell-Off · Full Day)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab6:
    st.markdown("## Michael T. — Full Day · June 3, 2026")
    st.caption("Voicemail → Phone call → Email → Text → Thursday meeting · PHLX -8.1% scenario")

    st.markdown("""
    <div style="background:#F0FDF4;border-left:4px solid #065F46;padding:12px 16px;
                border-radius:6px;margin-bottom:20px;font-size:13px;color:#1A1A2E">
      This tab shows how a single market event moves through a full advisor-client day.
      Every exchange below would be encoded as new nodes in Michael's memory graph.
    </div>
    """, unsafe_allow_html=True)

    # ── Voicemail ─────────────────────────────────────────────────────────────
    st.markdown("### 📞 Voicemail from Michael — 9:52 AM")
    vm = VOICEMAIL
    st.markdown(f"""
    <div style="background:#1A1A2E;border-radius:8px;padding:18px 22px;margin-bottom:8px">
      <div style="display:flex;justify-content:space-between">
        <span style="color:#94A3B8;font-size:12px">From: {vm['from']}  ·  {vm['time']}  ·  {vm['duration']}</span>
      </div>
      <p style="color:#E2E8F0;font-style:italic;margin:12px 0 0 0">"{vm['transcript']}"</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <p style="font-size:12px;color:#7C3AED;margin:0 0 20px 4px">
      📍 <em>Advisor read: {vm['advisor_read']}</em>
    </p>
    """, unsafe_allow_html=True)

    # ── Advisor Prep ──────────────────────────────────────────────────────────
    st.markdown("### 📋 Advisor Prep Notes — 10:14 AM")
    st.caption(f"Memory graph reviewed · {ADVISOR_PREP['duration']} before calling back")
    for note in ADVISOR_PREP["notes"]:
        color = "#CC2200" if note.startswith("DO NOT") else (
                "#003087" if note.startswith("KEY") or note.startswith("TARGET") or note.startswith("OPEN") else
                "#1A1A2E")
        st.markdown(
            f'<p style="font-size:13px;color:{color};margin:4px 0 4px 8px">— {note}</p>',
            unsafe_allow_html=True,
        )

    st.divider()

    # ── Phone Call ────────────────────────────────────────────────────────────
    st.markdown("### 📞 Phone Call — 10:17 AM · 9 minutes")

    for turn in PHONE_CALL:
        is_advisor = "Advisor" in turn["speaker"]
        bg     = "#EFF6FF" if is_advisor else "#F8FAFC"
        border = "#003087" if is_advisor else "#475569"
        label  = f"**{turn['speaker']}** · {turn['time']}"

        st.markdown(f"""
        <div style="background:{bg};border-left:4px solid {border};
                    padding:12px 16px;border-radius:6px;margin-bottom:6px">
          <p style="font-size:11px;color:#64748B;margin:0 0 6px 0">{label}</p>
          <p style="margin:0;color:#1A1A2E;font-size:14px;line-height:1.6">{turn['text']}</p>
        </div>
        """, unsafe_allow_html=True)

        if turn.get("subtext"):
            st.markdown(
                f"<p style='font-size:11px;color:#7C3AED;margin:-2px 0 10px 20px'>"
                f"📍 <em>{turn['subtext']}</em></p>",
                unsafe_allow_html=True,
            )

    st.divider()

    # ── Follow-Up Email ───────────────────────────────────────────────────────
    st.markdown("### ✉️ Follow-Up Email — 11:45 AM")
    em = FOLLOW_UP_EMAIL
    st.markdown(f"""
    <div class="client-card" style="font-family:monospace">
      <p style="font-size:11px;color:#64748B;margin:0">
        <strong>From:</strong> {em['from']}<br>
        <strong>To:</strong> {em['to']}<br>
        <strong>Subject:</strong> {em['subject']}
      </p>
      <hr style="border-color:#eee;margin:10px 0">
      <pre style="font-family:inherit;font-size:13px;color:#1A1A2E;white-space:pre-wrap;margin:0">{em['body']}</pre>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── Text Exchange ─────────────────────────────────────────────────────────
    st.markdown("### 💬 Text Exchange — 6:14 PM")
    st.caption("After Michael spoke to Susan at home")

    for msg in TEXT_EXCHANGE:
        is_advisor = "Advisor" in msg["from"]
        align = "flex-end" if is_advisor else "flex-start"
        bg    = "#003087" if is_advisor else "#E2E8F0"
        color = "white"  if is_advisor else "#1A1A2E"
        name  = msg["from"]

        st.markdown(f"""
        <div style="display:flex;justify-content:{align};margin-bottom:8px">
          <div style="max-width:70%;background:{bg};color:{color};
                      padding:10px 14px;border-radius:12px;font-size:13px">
            <p style="font-size:10px;opacity:0.7;margin:0 0 4px 0">{name} · {msg['time']}</p>
            {msg['text']}
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── Thursday Meeting ──────────────────────────────────────────────────────
    st.markdown("### 🤝 Thursday Meeting — June 11, 2026 · 2:04 PM")
    tm = THURSDAY_MEETING
    st.caption(f"{tm['location']} · {', '.join(tm['attendees'])}")

    for turn in tm["opening_exchange"]:
        is_advisor = "Advisor" in turn["speaker"]
        bg     = "#EFF6FF" if is_advisor else "#F8FAFC"
        border = "#003087" if is_advisor else "#475569"
        st.markdown(f"""
        <div style="background:{bg};border-left:4px solid {border};
                    padding:12px 16px;border-radius:6px;margin-bottom:6px">
          <p style="font-size:11px;color:#64748B;margin:0 0 6px 0"><strong>{turn['speaker']}</strong></p>
          <p style="margin:0;color:#1A1A2E;font-size:14px;line-height:1.6">{turn['text']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("**Meeting agenda**")
    for item in tm["agenda"]:
        st.markdown(f"- {item}")

    st.divider()

    # ── New Graph Nodes ───────────────────────────────────────────────────────
    st.markdown("### 🧠 New Memory Nodes — What This Day Added to the Graph")
    col_n, col_e = st.columns([1, 1])

    with col_n:
        st.markdown("**New nodes**")
        for n in NEW_GRAPH_NODES:
            color = NODE_COLORS.get(n["type"], "#888")
            st.markdown(
                f'<span class="node-chip" style="background:{color}">{n["type"]}</span> '
                f'<code style="font-size:11px">{n["label"].replace("_"," ")}</code>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<p style="font-size:11px;color:#64748B;margin:0 0 10px 10px">{n["summary"]}</p>',
                unsafe_allow_html=True,
            )

    with col_e:
        st.markdown("**New edges**")
        for src, rel, tgt in NEW_GRAPH_EDGES:
            st.markdown(
                f'<code style="font-size:11px">{src.replace("_"," ")}</code>'
                f'<span style="color:#C8A034;font-weight:700"> → {rel} → </span>'
                f'<code style="font-size:11px">{tgt.replace("_"," ")}</code>',
                unsafe_allow_html=True,
            )
            st.markdown("")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 7 — HuggingFace Real Data (hidden — toggle 🔬 in sidebar to reveal)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if tab7 is not None:
    with tab7:
        st.markdown("## Real Dataset — Conv-FinRe / hub24")
        data_source = "🟢 Live from HuggingFace Hub" if hf_live else "🟡 Bundled sample rows (Conv-FinRe schema)"
        st.markdown(
            f"<div style='background:#F0FDF4;border-left:4px solid #065F46;padding:10px 16px;"
            f"border-radius:6px;margin-bottom:20px;font-size:13px;color:#1A1A2E'>"
            f"<strong>Data source:</strong> {data_source} &nbsp;·&nbsp; "
            f"<strong>Dataset:</strong> TheFinAI/conv-finre &nbsp;·&nbsp; "
            f"<strong>Split:</strong> test · 230 rows"
            f"</div>",
            unsafe_allow_html=True,
        )

        # ── SECTION A: Raw rows (what HuggingFace actually contains) ──────────
        st.markdown("### Step 1 — What the raw dataset looks like")
        st.markdown(
            "<p style='font-size:13px;color:#475569;margin-bottom:12px'>"
            "This is what you see at <code>huggingface.co/datasets/TheFinAI/conv-finre</code> — "
            "columns: <code>id</code> · <code>user_id</code> · <code>step</code> · <code>date</code> · "
            "<code>messages</code> · <code>labels</code> · <code>meta</code> · <code>prompt</code>"
            "</p>",
            unsafe_allow_html=True,
        )

        for raw in HF_RAW_ROWS:
            with st.expander(
                f"🗂️  {raw['id']}  ·  {raw['date']}  ·  step {raw['step']}",
                expanded=(raw["step"] == 9),
            ):
                col_left, col_right = st.columns([1, 1])

                with col_left:
                    st.markdown("**`messages` — the conversation**")
                    for msg in raw["messages"]:
                        is_adv = msg["role"] == "advisor"
                        bg     = "#EFF6FF" if is_adv else "#F8FAFC"
                        border = "#003087" if is_adv else "#475569"
                        role   = "Advisor" if is_adv else "Client"
                        st.markdown(
                            f"<div style='background:{bg};border-left:3px solid {border};"
                            f"padding:8px 12px;border-radius:5px;margin-bottom:6px'>"
                            f"<p style='font-size:10px;color:#64748B;margin:0 0 3px 0'><strong>{role}</strong></p>"
                            f"<p style='font-size:12px;color:#1A1A2E;margin:0'>{msg['content']}</p>"
                            f"</div>",
                            unsafe_allow_html=True,
                        )

                    st.markdown("**`prompt` — what gets sent to the LLM**")
                    st.markdown(
                        f"<div style='background:#1A1A2E;padding:10px 14px;border-radius:6px'>"
                        f"<p style='font-size:11px;color:#94A3B8;margin:0;font-family:monospace'>{raw['prompt']}</p>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )

                with col_right:
                    st.markdown("**`labels` — three competing ground truths**")

                    label_meta = [
                        ("momentum_rank",    "#991B1B", "What price momentum says to buy"),
                        ("utility_rank",     "#065F46", "What's rational for this client's risk profile"),
                        ("user_choice_rank", "#1D4ED8", "What the client actually chose"),
                    ]
                    for key, col, desc in label_meta:
                        tickers = raw["labels"].get(key, [])
                        st.markdown(
                            f"<div style='background:white;border-left:3px solid {col};"
                            f"padding:8px 12px;border-radius:5px;margin-bottom:8px;"
                            f"box-shadow:0 1px 3px rgba(0,0,0,0.06)'>"
                            f"<p style='font-size:10px;color:{col};font-weight:700;margin:0 0 3px 0'>"
                            f"<code>{key}</code></p>"
                            f"<p style='font-size:11px;color:#64748B;margin:0 0 5px 0'>{desc}</p>"
                            f"<p style='font-size:13px;font-weight:600;color:#1A1A2E;margin:0'>"
                            f"{'  →  '.join(tickers)}</p>"
                            f"</div>",
                            unsafe_allow_html=True,
                        )

                    st.markdown("**`meta` — context for the session**")
                    meta = raw["meta"]
                    st.markdown(
                        f"<div class='client-card'>"
                        f"<p style='font-size:12px;color:#64748B;margin:2px 0'>"
                        f"<strong>Candidate tickers:</strong> {', '.join(meta['candidate_tickers'])}</p>"
                        f"<p style='font-size:12px;color:#64748B;margin:2px 0'>"
                        f"<strong>Risk profile:</strong> {meta['user_risk_profile']}</p>"
                        f"<p style='font-size:12px;color:#64748B;margin:2px 0'>"
                        f"<strong>Horizon:</strong> {meta['horizon_days']} days</p>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )

        # ── SECTION B: The key insight — three rankings diverge ───────────────
        st.divider()
        st.markdown("### The key insight — three rankings, one client, same day")
        st.markdown(
            "<div style='background:#FFFBEB;border-left:4px solid #C8A034;padding:14px 18px;"
            "border-radius:6px;margin-bottom:16px;font-size:13px;color:#1A1A2E'>"
            "<strong>Step 11 (Aug 29):</strong> AMZN is up 3% pre-market. "
            "The three rankings completely disagree:<br><br>"
            "📈 <strong style='color:#991B1B'>Momentum says:</strong> TSLA #1, XOM #2, AMZN #3<br>"
            "🧠 <strong style='color:#065F46'>Utility says:</strong> JPM #1, XOM #2, MMM #3<br>"
            "👤 <strong style='color:#1D4ED8'>Client chose:</strong> JPM #1, XOM #2, TSLA #3<br><br>"
            "The client ignored the AMZN momentum, responded to JPM analyst upgrades, "
            "and stuck with XOM. That pattern — repeated across 3 sessions — is a <strong>behavioural signal</strong>. "
            "An LLM trained only on user_choice_rank would learn that pattern. "
            "An LLM trained only on momentum_rank would recommend TSLA and AMZN this client doesn't want."
            "</div>",
            unsafe_allow_html=True,
        )

        # ── SECTION C: What our system extracts ───────────────────────────────
        st.divider()
        st.markdown("### Step 2 — What our memory graph extracts from those 3 rows")
        st.markdown(
            "<p style='font-size:13px;color:#475569;margin-bottom:12px'>"
            "Our encoder reads the 3 sessions above and converts behavioural patterns "
            "into persistent memory nodes — so the advisor carries this forward to every future conversation."
            "</p>",
            unsafe_allow_html=True,
        )

        col_enc_n, col_enc_e = st.columns([1, 1])

        with col_enc_n:
            st.markdown("**Extracted nodes**")
            for n in HF_RAW_ENCODED["nodes"]:
                color = NODE_COLORS.get(n["type"], "#888")
                st.markdown(
                    f'<span class="node-chip" style="background:{color}">{n["type"]}</span> '
                    f'<code style="font-size:11px">{n["label"].replace("_"," ")}</code>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<p style="font-size:11px;color:#64748B;margin:0 0 10px 12px">{n["summary"]}</p>',
                    unsafe_allow_html=True,
                )

            st.markdown("**Extracted edges**")
            for src, rel, tgt in HF_RAW_ENCODED["edges"]:
                st.markdown(
                    f'<code style="font-size:11px">{src.replace("_"," ")}</code>'
                    f'<span style="color:#C8A034;font-weight:700"> → {rel} → </span>'
                    f'<code style="font-size:11px">{tgt.replace("_"," ")}</code>',
                    unsafe_allow_html=True,
                )
                st.markdown("")

        with col_enc_e:
            st.markdown("**Advisor alert generated**")
            alert  = HF_RAW_ENCODED["advisor_alert"]
            action = alert["action"]
            icon, ac = ACTION_BADGE.get(action, ("⚪", "#888"))
            st.markdown(
                f"<div class='alert-card' style='border-left-color:{ac}'>"
                f"<span style='background:{ac};color:white;padding:2px 12px;"
                f"border-radius:12px;font-size:12px;font-weight:700'>{icon} {action}</span>"
                f"<p style='margin:8px 0 4px 0;font-size:13px;color:#1A1A2E'>"
                f"<strong>Trigger:</strong> {alert['trigger']}</p>"
                f"<p style='font-size:13px;color:#1A1A2E;margin:4px 0'>"
                f"<strong>Context:</strong> {alert['context']}</p>"
                f"<p style='font-size:13px;color:#003087;margin:4px 0'>"
                f"<strong>Approach:</strong> {alert['suggested_approach']}</p>"
                f"</div>",
                unsafe_allow_html=True,
            )

            st.markdown(
                "<div style='background:#F5F3FF;border-left:3px solid #7C3AED;"
                "padding:12px 16px;border-radius:6px;margin-top:16px;font-size:12px;color:#1A1A2E'>"
                "<strong>🔁 What this enables:</strong><br>"
                "Next time XOM drops on earnings, this client fires to the top of the alert queue. "
                "The advisor already knows: frame it around analyst opinion, not price action. "
                "That insight came from 3 rows of raw ranking data."
                "</div>",
                unsafe_allow_html=True,
            )

        st.divider()
        st.markdown("### Step 3 — Deeper client profiles (Conv-FinRe onboarding style)")
        st.markdown(
            "<p style='font-size:13px;color:#475569;margin-bottom:16px'>"
            "The dataset also includes onboarding interviews — a 4-turn dialogue that captures "
            "each investor's background, goals, and risk reactions before any stock ranking begins."
            "</p>",
            unsafe_allow_html=True,
        )

        RISK_COLORS = {
            "Conservative": "#065F46",
            "Moderate":     "#1D4ED8",
            "Aggressive":   "#991B1B",
        }

        for client in hf_clients:
            uid       = client["user_id"]
            source    = client["source"]
            risk      = client["risk_profile"]
            age       = client["age_bracket"]
            risk_col  = RISK_COLORS.get(risk, "#444")
            onboard   = client["onboarding"]

            st.markdown(
                f"<div style='background:white;border-left:5px solid {risk_col};"
                f"padding:14px 20px;border-radius:8px;margin-bottom:6px;"
                f"box-shadow:0 1px 4px rgba(0,0,0,0.07)'>"
                f"<div style='display:flex;justify-content:space-between;align-items:center'>"
                f"<span style='font-size:18px;font-weight:700;color:#003087'>{uid}</span>"
                f"<span style='background:{risk_col};color:white;padding:2px 12px;"
                f"border-radius:12px;font-size:12px;font-weight:600'>{risk}</span>"
                f"</div>"
                f"<p style='color:#64748B;font-size:12px;margin:4px 0 0 0'>"
                f"Age {age} &nbsp;·&nbsp; {source}</p>"
                f"</div>",
                unsafe_allow_html=True,
            )

            with st.expander(f"📋 {uid} — Onboarding + Conversation", expanded=False):
                col_ob, col_cv = st.columns([1, 1])

                with col_ob:
                    st.markdown("**Onboarding profile**")
                    st.markdown(
                        f"<div class='client-card'>"
                        f"<p style='font-size:13px;color:#1A1A2E;margin:0 0 8px 0'>{onboard['background']}</p>"
                        f"<p style='font-size:12px;color:#64748B;margin:4px 0'>"
                        f"<strong>Risk tolerance:</strong> {onboard['stated_risk_tolerance']}</p>"
                        f"<p style='font-size:12px;color:#64748B;margin:4px 0'>"
                        f"<strong>Horizon:</strong> {onboard['investment_horizon']}</p>"
                        f"<p style='font-size:12px;color:#64748B;margin:4px 0'>"
                        f"<strong>Experience:</strong> {onboard['prior_experience']}</p>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )

                    st.markdown("**Pre-encoded nodes**")
                    for n in client["encoded_nodes"]:
                        color = NODE_COLORS.get(n["type"], "#888")
                        st.markdown(
                            f'<span class="node-chip" style="background:{color}">'
                            f'{n["type"]}</span> '
                            f'<code style="font-size:11px">{n["label"].replace("_"," ")}</code>',
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            f'<p style="font-size:11px;color:#64748B;margin:0 0 8px 12px">'
                            f'{n["summary"]}</p>',
                            unsafe_allow_html=True,
                        )

                    st.markdown("**Edges**")
                    for src, rel, tgt in client["encoded_edges"]:
                        st.markdown(
                            f'<code style="font-size:11px">{src.replace("_"," ")}</code>'
                            f'<span style="color:#C8A034;font-weight:700"> → {rel} → </span>'
                            f'<code style="font-size:11px">{tgt.replace("_"," ")}</code>',
                            unsafe_allow_html=True,
                        )
                        st.markdown("")

                with col_cv:
                    st.markdown("**Advisory dialogue**")
                    for turn in client["conversations"]:
                        is_advisor = turn["role"] == "advisor"
                        bg     = "#EFF6FF" if is_advisor else "#F8FAFC"
                        border = "#003087" if is_advisor else "#475569"
                        label  = f"**Advisor** · Turn {turn['turn']}" if is_advisor else f"**Client** · Turn {turn['turn']}"
                        st.markdown(
                            f"<div style='background:{bg};border-left:4px solid {border};"
                            f"padding:10px 14px;border-radius:6px;margin-bottom:8px'>"
                            f"<p style='font-size:11px;color:#64748B;margin:0 0 4px 0'>{label}</p>"
                            f"<p style='margin:0;color:#1A1A2E;font-size:13px;line-height:1.6'>{turn['text']}</p>"
                            f"</div>",
                            unsafe_allow_html=True,
                        )

                    st.markdown("**Advisor alert**")
                    alert   = client["advisor_alert"]
                    action  = alert["action"]
                    icon, ac = ACTION_BADGE.get(action, ("⚪", "#888"))
                    st.markdown(
                        f"<div class='alert-card' style='border-left-color:{ac}'>"
                        f"<span style='background:{ac};color:white;padding:2px 12px;"
                        f"border-radius:12px;font-size:12px;font-weight:700'>{icon} {action}</span>"
                        f"<p style='margin:8px 0 4px 0;font-size:13px;color:#1A1A2E'>"
                        f"<strong>Trigger:</strong> {alert['trigger']}</p>"
                        f"<p style='font-size:13px;color:#1A1A2E;margin:4px 0'>"
                        f"<strong>Context:</strong> {alert['context']}</p>"
                        f"<p style='font-size:13px;color:#003087;margin:4px 0'>"
                        f"<strong>Approach:</strong> {alert['suggested_approach']}</p>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
