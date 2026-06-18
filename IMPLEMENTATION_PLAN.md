# Implementation Plan
### RJ MemoryAlpha · Raymond James Engineering Challenge 2026

---

## Phase 1 — Proof of Concept *(done — live demo exists)*

- Build graph engine using Python + NetworkX
- Create synthetic client datasets (8 clients, behavioral archetypes)
- Develop Streamlit dashboard for memory visualization and market alerts
- Store graph data in JSON
- **Live demo:** https://memory-graph-sc-v3.streamlit.app/

---

## Phase 2 — Intelligence & Triggering

- Integrate market event triggers (S&P drop, Fed announcements, sector news)
- Build alert engine to identify which clients are impacted by each event
- Add rule-based recommendation layer: who to call, why, and what to say
- Browser AI agent: Chrome extension that reads any advisor workflow page and
  answers questions about client context using the memory graph

---

## Phase 3 — AI Integration

- Use Claude API to convert meeting notes into structured graph nodes
- Deploy Persona AI layer: advisor profile + writing sample injection + client
  graph context composed before every LLM call
- The advisor profile is not static — it updates continuously as the advisor
  approves and sends communications, so the persona sharpens from their own
  usage over time with no manual configuration required
- Deploy XAI layer: SHAP-style node attribution + counterfactual generation +
  per-recommendation compliance log stored with full prompt and graph context
- Human-in-the-loop: advisor reviews every AI draft before it reaches any client

---

## Phase 4 — Enterprise Integration

- Integrate with existing Raymond James CRM systems
- Implement secure data storage (AWS-based architecture aligned with firm standards)
- Replace ChromaDB (demo only) with RJ-hosted vector store — no client PII
  leaves firm infrastructure
- FINRA audit log pipeline: every AI-assisted recommendation stored with
  attribution, composed prompt, and counterfactual
  Reference: https://www.finra.org/rules-guidance/notices/24-09

---

## What to Update in the Submission Portal

| Section | What to add or change |
|---|---|
| **Phase 1** | Add live demo link: memory-graph-sc-v3.streamlit.app |
| **Phase 2** | Add browser AI agent bullet |
| **Phase 3** | Replace existing 2 bullets with: Persona AI + self-updating profile + XAI + human-in-the-loop |
| **Phase 4** | Add ChromaDB → RJ-hosted vector store bullet + FINRA audit log pipeline bullet |
