# RJ MemoryAlpha — Client Financial Memory Graph
### Raymond James Engineering Challenge 2026 · Submission by Surya Teja Meesala

---

## Business Problem

Financial advisors at Raymond James often manage relationships with 150–300+ clients, making it extremely difficult to retain nuanced, individualized context about each client over time. While current CRM systems effectively store transactional data and meeting notes, they fall short in capturing **how a client thinks, feels, and evolves behaviorally**.

In practice, critical insights such as a client's emotional response to volatility, regret from past decisions, or conviction in certain sectors are buried within unstructured notes. For example, when a client says *"I sold everything in 2020 and it was my biggest mistake,"* that insight is stored as static text rather than a reusable, structured memory that can guide future advisor actions.

This leads to:
- Missed opportunities to proactively engage clients during market events
- Generic or reactive advisory interactions rather than personalized guidance
- Inconsistent advisor experience, especially when managing large books of business
- Loss of behavioral insights during advisor transitions or team collaboration

Today, even when this behavioral memory exists in notes, advisors cannot access it at the moment they need it. When an advisor opens a client statement, a portfolio tool, or a market alert — that context is buried in a separate system. The cost of this gap is measured in missed calls during market events, generic outreach that ignores client history, and lost trust when an advisor forgets what a client told them two years ago.

DALBAR research consistently shows that behavioral coaching — not investment selection — is the primary driver of advisor alpha. Yet no structured system exists to capture or operationalize this coaching context at scale.

Industry research (e.g., Dalbar QAIB, Vanguard Advisor's Alpha) consistently shows that **client behavior — not market performance — is a major driver of poor financial outcomes**, highlighting a clear unmet need for systems that operationalize behavioral context.

This challenge directly aligns with recent leadership messaging from Raymond James. In a **Nov 12, 2025 CNBC interview**, CEO Paul Shoukry emphasized that:
- Advisors play a critical role in helping clients **avoid emotional, knee-jerk reactions to market events**
- The firm's strategy is centered on the **"power of personal"** — deep, trusted relationships between advisors and clients that go beyond transactions
- Technology and AI should **enhance — not replace** these deeply personal relationships

However, today there is no structured system that helps advisors **retain, recall, and operationalize this depth of behavioral understanding at scale.**

---

## Proposed Idea

The proposed solution is a **Client Financial Memory Graph** — a structured, dynamic knowledge layer that models each advisor-client relationship as an evolving graph.

Instead of storing notes as unstructured text, this system converts advisor-client conversations into meaningful, connected data elements:

- **Belief Nodes** — what the client believes (e.g., "tech always rebounds")
- **Emotion Nodes** — emotional reactions (e.g., fear during a downturn)
- **Action Nodes** — what the client did (e.g., sold equities in March 2020)
- **Event Nodes** — external triggers (e.g., COVID crash, Fed rate hikes)
- **Temporal Edges** — relationships that track how these evolve over time

Using this structure, the system enables **context-aware intelligence**:
- During market volatility, it surfaces **which clients are likely to react emotionally**
- Provides advisors with **personalized talking points grounded in the client's own words**
- Identifies behavioral patterns such as regret cycles, risk aversion, or sector bias

A lightweight AI layer (Claude API) converts meeting notes into graph nodes, ensuring minimal friction for advisors. A **dashboard** enables visualization of client memory timelines and proactive alerting.

### Browser-Native AI Agent

To close the access gap, we built a **browser-native AI agent** — a Chrome extension side panel that works on any webpage the advisor has open. The advisor types a question in plain English. The agent reads the current screen, navigates it autonomously, and surfaces the relevant memory from the graph. It requires no tool switching, no training, and no new login. It works on any RJ internal tool today.

The agent can:
- Scroll through pages, click tabs, and capture screenshots autonomously
- Answer questions like *"Given the S&P dropped 5% today, which clients should I call first and why?"*
- Surface client behavioral memory at the exact moment of need — on whatever screen the advisor is already using
- Work across any advisor-facing tool: CRM, portfolio systems, research pages, internal dashboards

**Live POC Demo:** [View Client Financial Memory Graph Demo](https://memorygraphforfas.streamlit.app/)

This working prototype demonstrates:
- Client memory visualization
- Behavioral node relationships
- Market-triggered advisor alerts
- Live browser AI agent scanning and answering questions from any page

---

## Relevance to the Firm

This solution directly aligns with Raymond James' client-first philosophy and enhances both advisor effectiveness and client outcomes.

### For Advisors:
- Transforms CRM from a passive system into an **active decision-support tool**
- Reduces cognitive load by externalizing client memory into a structured system
- Enables **highly personalized, timely outreach during key market events**
- Surfaces behavioral memory at the exact moment of need — on whatever screen the advisor is already using
- Eliminates the context-switching tax of managing 150–300 clients across multiple tools
- Works across any internal RJ system without requiring platform integration in Phase 1

### For Clients:
- Receive advice that reflects their **unique history, behavior, and preferences**
- Improved trust and relationship depth through continuity of understanding
- Reduced likelihood of emotionally driven investment mistakes

### For the Firm:
- Creates a **differentiated advisory experience** vs competitors relying on traditional CRM
- Improves retention by strengthening advisor-client relationships
- Captures institutional knowledge that persists beyond individual advisors
- Establishes a foundation for future AI-driven advisory capabilities
- The browser agent architecture means zero dependency on CRM vendor timelines — it layers on top of existing systems immediately
- Positions RJ ahead of competitors who are building AI inside single tools rather than across the entire advisor workflow

This positions Raymond James as a leader in **behavior-aware wealth management**, moving beyond portfolio performance into behavioral optimization.

---

## Implementation

### Phase 1 — Proof of Concept ✅ COMPLETE
- Build graph engine using Python + NetworkX
- Create synthetic client datasets (8 archetypes, 65 nodes, 95 edges)
- Develop dashboard for visualization and alerts
- Store graph data in JSON
- Build browser-native AI agent (Chrome extension) with live page scanning

### Phase 2 — Intelligence & Triggering
- Integrate market event triggers (e.g., S&P drop, Fed announcements)
- Build alert engine to identify impacted clients
- Add rule-based recommendation layer for advisor guidance

### Phase 3 — AI Integration
- Use LLM (Claude API) to convert meeting notes into structured graph nodes
- Ensure a human-in-the-loop workflow where advisors review and approve entries
- Enable continuous learning from new client interactions
- Deploy browser-native AI agent that reads any advisor-facing page and queries the memory graph in real time
- Human-in-the-loop: every agent response requires advisor confirmation before any client action is taken

### Phase 4 — Enterprise Integration
- Integrate with existing Raymond James CRM systems
- Implement secure data storage (AWS-based architecture aligned with firm standards)
- Publish extension via RJ-managed Chrome deployment (MDM) — no App Store approval required, zero friction rollout to all advisors
- Route all AI calls through RJ enterprise API proxy with zero data retention agreement — no client data leaves firm infrastructure

---

## Risks & Mitigations

### Data Accuracy & Integrity
- **Risk:** Incorrect interpretation of client statements by AI
- **Mitigation:** Strict human-in-the-loop validation before storing any data

### AI Agent & Compliance (FINRA / SEC Reg S-P)
- **Risk:** Agent reads client data on screen and sends it to an external AI API
- **Mitigation:** All API calls route through an RJ-hosted proxy. Client PII is stripped before leaving the internal network. Every query and response is logged to the supervision audit trail per FINRA Rule 3110. The agent surfaces information only — it cannot execute trades, send communications, or take any action without explicit advisor approval.

### Suitability Liability (FINRA Rule 2111)
- **Risk:** AI output could be construed as a suitability recommendation
- **Mitigation:** Every output is labeled as decision-support, not a recommendation. Advisor review is mandatory before any client action.

---

## How to Sharpen This Idea Further

*Internal notes for refinement before final submission:*

### 1. Name the real problem in RJ's language
Find out what advisors internally call this pain point. "Client context switching," "relationship continuity," or "behavioral memory loss." Use their words in the submission, not tech words.

### 2. Add one quantified stat
Find a number specific to RJ or the industry:
- Average number of clients per advisor at RJ
- Time advisors spend on pre-call research per client
- Client attrition rate following market events with no proactive outreach
Even one credible number makes the problem undeniable.

### 3. Show it on a real RJ tool in the demo
Currently the demo runs on a custom Streamlit app. For the presentation, show the browser agent working on something that looks like an actual advisor workflow — even a mock of an internal portal or a client statement PDF. The closer to their real tools, the smaller the gap between POC and production feels to judges.

### 4. Add a one-slide roadmap moment
Show judges what this looks like if funded:
- **Now:** Memory graph + browser agent (done)
- **6 months:** Integrated into RJ internal advisor portal
- **12 months:** Proactive push alerts before market open, mobile companion

### 5. Identify RJ's actual CRM
RJ likely uses Tamarac, Redtail, or a proprietary system. Name it explicitly and show the gap. Specificity stands out against generic submissions.

### 6. Competitive moat statement
Add one line that shows this is defensible:
> *"The graph structure means every new client interaction makes the system smarter — it compounds over time in a way a flat CRM note system never can."*

### 7. Pilot proposal
End the submission with a concrete ask:
> *"We propose a 90-day pilot with 10 advisors across one branch. Success metric: reduction in pre-call research time and increase in proactive client outreach during market events."*
A specific pilot ask signals you've thought past the idea into execution.
