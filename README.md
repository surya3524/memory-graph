# Client Financial Memory Graph

> A living, structured memory layer for every advisor–client relationship —  
> built for the Raymond James Engineering Challenge 2026.

---

## The Problem

A financial advisor with 200+ clients cannot hold nuanced client context in their head. Today's CRM is a static notes dump — it stores facts but not beliefs, emotions, or how a client's thinking has evolved over time.

When a client says *"I sold everything in 2020 and it was my biggest mistake"* — that should become a node in a graph that connects to a market event, an emotion, a regret, and a future action trigger. Not a paragraph buried in a PDF.

## What This Builds

A **graph memory architecture** where every client has:

- **Belief nodes** — what they've stated they believe
- **Emotion nodes** — how they've responded to market events
- **Action nodes** — what they actually did
- **Event nodes** — the market moments that shaped them
- **Temporal edges** — how all of the above connect and evolve over time

When volatility hits, the system surfaces: *who to call, why, and exactly what to say* — grounded in that client's own words from prior meetings.

## Client Archetypes (8 Synthetic Demo Clients)

| Client | Archetype | Alert Trigger |
|--------|-----------|---------------|
| John M. | Regretful Seller | Market drop >5% |
| Sarah K. | Capital Preserver | Recession news / Fed decisions |
| Michael T. | Sector Believer — Semiconductors | Taiwan news / China export controls |
| Bobby H. | Sector Believer — Oil & Gas | Oil drop >15% / Energy policy |
| Linda P. | Inflation Hedge Seeker | Fed stimulus / Dollar weakness |
| Carol & Jim B. | Near-Retiree Couple | Market drop within 24mo of retirement |
| Marcus W. | Sudden Wealth — Inheritance | 12-month inaction flag |
| Priya N. | DIY Defector | Portfolio underperforms S&P by >2% |

Archetypes are grounded in behavioral finance research:
- Dalbar QAIB (annual investor behavior report)
- Morningstar "Mind the Gap" (2023)
- Vanguard Advisor's Alpha (2022)

## Ethical Design

This system encodes **only what clients explicitly stated** in advisor meetings.

- No demographic inference
- No psychological profiling
- No data the client did not disclose
- Advisor reviews and owns all entries

> Core principle: the graph encodes what the client said, not who we think they are.

## Stack

```
Graph engine:   Python + NetworkX
AI layer:       Claude API (meeting note → graph node encoding)
Dashboard:      Streamlit
Storage:        JSON (no database required for POC)
```

## Getting Started

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Set up your API key** *(only needed for the Note Encoder tab)*
```bash
cp .env.example .env
# Open .env and paste your key from https://console.anthropic.com
```

**3. Run the dashboard**
```bash
ANTHROPIC_API_KEY=$(grep ANTHROPIC_API_KEY .env | cut -d= -f2) streamlit run dashboard.py
```

The Market Alerts, Client Graph, and Memory Timeline tabs work with **no API key**.
The Note Encoder tab uses Claude to parse meeting notes — that's the only part that needs one.

> **Cost:** encoding one meeting note costs less than $0.01. A full demo day is under $1.

## Project Structure

```
sample_clients.py   — 8 synthetic client histories with nodes, edges, alerts
graph_engine.py     — graph builder and query engine      (coming in phase 1)
trigger.py          — market event → advisor alert system (coming in phase 2)
encoder.py          — meeting note → graph node via Claude API (coming in phase 3)
dashboard.py        — Streamlit advisor UI                (coming in phase 3)
```

---

*POC proposal — Raymond James Engineering Challenge 2026*
