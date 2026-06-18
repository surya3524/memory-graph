# RJ Client Financial Memory Graph — Persona AI + Explainable AI
## Technical Specification for Claude Code

---

## 1. WHAT WE ARE BUILDING

A full-stack web application demonstrating three integrated AI capabilities for Raymond James financial advisors:

1. **Client Financial Memory Graph** — A knowledge graph of each client's financial life (goals, risk profile, behavioral patterns, life events, transaction history). The graph is the intelligence layer that knows each client as a connected structure, not just a flat CRM record.

2. **Advisor Persona AI** — Every AI prompt the advisor sends is automatically enriched with their persona (communication style, specialty, tone, client base) before hitting the LLM. The advisor gets responses that sound like THEM — not a generic financial AI.

3. **Explainable AI (XAI) Layer** — Every AI recommendation surfaces which graph nodes drove it (SHAP-style attribution) and what would have changed the recommendation (counterfactual). This satisfies FINRA's 2026 requirement that AI-assisted advice must be explainable.

**Competitive differentiation from Altruist Hazel:** Hazel is a RAG system over documents. This system uses a structured knowledge graph enabling relationship traversal, behavioral pattern detection, and graph-level reasoning — fundamentally different capabilities.

---

## 2. MVP SCOPE (Innovation Challenge Demo)

Build a working demo that shows this full flow:

```
Advisor selects client
       ↓
Memory graph loads client context (goals, drift, behavior)
       ↓
Advisor types a prompt ("Write Q2 portfolio review email")
       ↓
System composes: [Advisor Persona] + [Client Graph Context] + [Prompt]
       ↓
Composed prompt hits Claude API
       ↓
Response rendered in advisor's voice
       ↓
Explainability panel shows: which graph nodes drove the response + counterfactual
```

---

## 3. TECH STACK

### Backend (Python)
```
fastapi==0.115.0
uvicorn==0.30.0
anthropic==0.40.0
networkx==3.4.2          # knowledge graph (demo) — Neo4j in production
sentence-transformers==3.2.0  # embeddings for persona RAG
chromadb==0.5.0          # vector store for advisor communications
numpy==1.26.0
pydantic==2.8.0
python-dotenv==1.0.0
```

### Frontend (React)
```
react + vite
tailwindcss (CDN)
d3 (graph visualization)
recharts (SHAP bar chart visualization)
```

### Environment Variables (.env)
```
ANTHROPIC_API_KEY=your_key_here
MODEL=claude-sonnet-4-6
MAX_TOKENS=1500
```

---

## 4. PROJECT FILE STRUCTURE

```
rj-persona-xai/
├── backend/
│   ├── main.py                  # FastAPI app, all routes
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── client_graph.py      # NetworkX knowledge graph
│   │   └── sample_data.py       # Mock client/advisor data
│   ├── persona/
│   │   ├── __init__.py
│   │   ├── persona_builder.py   # Builds advisor system prompt
│   │   └── persona_store.py     # Stores advisor profiles + comm samples
│   ├── xai/
│   │   ├── __init__.py
│   │   └── explainer.py         # SHAP simulation + counterfactual
│   ├── llm/
│   │   ├── __init__.py
│   │   └── claude_client.py     # Anthropic API wrapper
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── AdvisorPanel.jsx      # Advisor profile + prompt input
│   │   │   ├── ClientGraphPanel.jsx  # D3 graph visualization
│   │   │   ├── PersonaBuilder.jsx    # Shows composed system prompt live
│   │   │   ├── ResponsePanel.jsx     # AI response output
│   │   │   └── ExplainPanel.jsx      # SHAP chart + counterfactual
│   │   └── api/
│   │       └── client.js             # API calls to backend
└── README.md
```

---

## 5. DATA MODELS

### AdvisorProfile
```python
class AdvisorProfile(BaseModel):
    advisor_id: str           # "ADV001"
    name: str                 # "Surya T. Meesala"
    crd: str                  # "RJ-7832104"
    branch: str               # "St. Petersburg, FL"
    specialty: list[str]      # ["Treasury", "HNW clients", "Retirement"]
    communication_style: str  # "data-first, concise, technical depth"
    tone: str                 # "direct, professional, avoids jargon"
    client_demographics: str  # "Ages 45-68, $1M-$5M AUM"
    relationship_style: str   # "proactive, weekly for top-tier"
    compliance_scope: str     # "New Mexico registered, no discretionary authority"
    sample_communications: list[str]  # Past emails advisor wrote (for RAG)
```

### ClientGraphNode
```python
class GraphNode(BaseModel):
    node_id: str
    node_type: str    # "goal" | "risk_profile" | "life_event" | "portfolio" | "behavior" | "transaction"
    label: str        # "Retire at 65"
    value: Any        # The actual data
    weight: float     # 0.0-1.0, importance to this client
    timestamp: str    # When this node was last updated
```

### ClientGraphEdge
```python
class GraphEdge(BaseModel):
    source: str       # node_id
    target: str       # node_id
    relationship: str # "HAS_GOAL" | "DRIVES_RECOMMENDATION" | "CONFLICTS_WITH" etc.
    strength: float   # 0.0-1.0
```

### ClientGraph
```python
class ClientGraph(BaseModel):
    client_id: str
    client_name: str
    account: str
    nodes: list[GraphNode]
    edges: list[GraphEdge]
```

### PromptRequest
```python
class PromptRequest(BaseModel):
    advisor_id: str
    client_id: str
    user_prompt: str
```

### XAIResult
```python
class XAIResult(BaseModel):
    node_attributions: list[dict]  # [{node_id, label, shap_value, contribution_pct}]
    top_drivers: list[str]         # Plain-English top 3 drivers
    counterfactual: str            # "If X were Y, recommendation would be Z"
    confidence: float              # 0.0-1.0
```

### ApiResponse
```python
class ApiResponse(BaseModel):
    composed_prompt: str           # Full prompt sent to Claude (for transparency UI)
    persona_injected: dict         # Which persona fields were used
    graph_context_used: list[str]  # Which graph nodes were included
    llm_response: str              # Claude's actual response
    xai_result: XAIResult          # Explainability breakdown
    tokens_used: int
```

---

## 6. SAMPLE DATA

### Advisors
```python
ADVISORS = {
    "ADV001": {
        "advisor_id": "ADV001",
        "name": "Surya T. Meesala",
        "crd": "RJ-7832104",
        "branch": "St. Petersburg, FL",
        "specialty": ["Treasury Wires", "HNW clients", "Retirement Planning"],
        "communication_style": "data-first, concise, leads with key numbers",
        "tone": "direct and professional, avoids filler phrases",
        "client_demographics": "Ages 45-68, $1M-$5M AUM, moderate-aggressive risk",
        "relationship_style": "proactive outreach, weekly for top-tier clients",
        "compliance_scope": "New Mexico registered, no discretionary authority",
        "sample_communications": [
            "Margaret — quick update on your Q2 allocation. Your equity drift came in at 8.2%, above your 7% threshold. Here is what I recommend and why: [data-driven explanation]. Let me know if you want to discuss before we act.",
            "David — your RMD deadline is December 31. Based on your current balance of $1.4M and your age 73, the required distribution is $52,632. I have prepared three scenarios for how to handle this tax-efficiently. Call me this week.",
            "Priya — your wire to Fidelity cleared yesterday. Running balance in your RJ account is now $847,000. Your target allocation is still on track. Next review: September 15."
        ]
    },
    "ADV002": {
        "advisor_id": "ADV002",
        "name": "Jennifer Walsh",
        "crd": "RJ-5521089",
        "branch": "Albuquerque, NM",
        "specialty": ["Estate Planning", "Business Owners", "Philanthropic Planning"],
        "communication_style": "relationship-first, story-driven, warm",
        "tone": "conversational, empathetic, client-first language",
        "client_demographics": "Ages 55-75, $2M-$10M AUM, conservative risk",
        "relationship_style": "monthly touchpoints, family-office approach",
        "compliance_scope": "New Mexico registered, fee-only",
        "sample_communications": [
            "Hi Robert, I hope the family is doing well after the move to Santa Fe. I have been thinking about your estate plan given the change in domicile — there are a few things we should revisit before year-end that could make a real difference for the kids. When would be a good time to connect?",
            "Susan, thank you for sharing the news about the business sale. This is a wonderful milestone and I want to make sure we capture every opportunity to protect what you have built. I have sketched out three scenarios for the proceeds — let me walk you through them when you are ready."
        ]
    }
}
```

### Client Graphs
```python
CLIENT_GRAPHS = {
    "C001": {
        "client_id": "C001",
        "client_name": "Margaret Collins",
        "account": "RJ-**4821",
        "nodes": [
            {"node_id": "n1", "node_type": "goal", "label": "Retire at age 65", "value": {"target_age": 65, "current_age": 61, "years_remaining": 4}, "weight": 0.95, "timestamp": "2026-01-15"},
            {"node_id": "n2", "node_type": "risk_profile", "label": "Conservative risk tolerance", "value": {"score": 3, "scale": 10, "label": "Conservative"}, "weight": 0.85, "timestamp": "2026-03-01"},
            {"node_id": "n3", "node_type": "portfolio", "label": "Portfolio equity drift +8%", "value": {"target_equity": 55, "actual_equity": 63, "drift": 8.0, "aum": 1420000}, "weight": 0.90, "timestamp": "2026-06-17"},
            {"node_id": "n4", "node_type": "behavior", "label": "Accepted 3 prior rebalancings", "value": {"count": 3, "last_date": "2025-09-15", "pattern": "always accepts advisor recommendation"}, "weight": 0.75, "timestamp": "2025-09-15"},
            {"node_id": "n5", "node_type": "life_event", "label": "Spouse retired Jan 2026", "value": {"event": "spouse_retirement", "date": "2026-01-01", "income_impact": -45000}, "weight": 0.70, "timestamp": "2026-01-01"},
            {"node_id": "n6", "node_type": "transaction", "label": "Last wire: $25K to checking", "value": {"amount": 25000, "date": "2026-05-10", "type": "withdrawal", "frequency": "quarterly"}, "weight": 0.50, "timestamp": "2026-05-10"}
        ],
        "edges": [
            {"source": "n3", "target": "n1", "relationship": "THREATENS_GOAL", "strength": 0.88},
            {"source": "n2", "target": "n3", "relationship": "CONFLICTS_WITH", "strength": 0.85},
            {"source": "n4", "target": "n3", "relationship": "SUPPORTS_ACTION_ON", "strength": 0.75},
            {"source": "n5", "target": "n1", "relationship": "ACCELERATES_TIMELINE", "strength": 0.70}
        ]
    },
    "C002": {
        "client_id": "C002",
        "client_name": "David K. Thornton",
        "account": "RJ-**3367",
        "nodes": [
            {"node_id": "n1", "node_type": "goal", "label": "Fund children's education", "value": {"target": 350000, "current_529": 180000, "gap": 170000}, "weight": 0.90, "timestamp": "2025-11-20"},
            {"node_id": "n2", "node_type": "risk_profile", "label": "Moderate-aggressive risk", "value": {"score": 7, "scale": 10, "label": "Moderate-Aggressive"}, "weight": 0.80, "timestamp": "2026-02-10"},
            {"node_id": "n3", "node_type": "portfolio", "label": "Portfolio on target", "value": {"target_equity": 70, "actual_equity": 68, "drift": -2.0, "aum": 2100000}, "weight": 0.60, "timestamp": "2026-06-17"},
            {"node_id": "n4", "node_type": "life_event", "label": "Eldest child starting college 2027", "value": {"event": "college_start", "date": "2027-09-01", "annual_cost": 65000}, "weight": 0.92, "timestamp": "2025-09-01"},
            {"node_id": "n5", "node_type": "behavior", "label": "Prefers email communication", "value": {"preferred_channel": "email", "response_time": "same day", "meeting_frequency": "quarterly"}, "weight": 0.65, "timestamp": "2026-01-01"}
        ],
        "edges": [
            {"source": "n4", "target": "n1", "relationship": "TRIGGERS_ACTION_ON", "strength": 0.92},
            {"source": "n2", "target": "n3", "relationship": "CONSISTENT_WITH", "strength": 0.80},
            {"source": "n3", "target": "n1", "relationship": "SUPPORTS_GOAL", "strength": 0.70}
        ]
    },
    "C003": {
        "client_id": "C003",
        "client_name": "Priya S. Nair",
        "account": "RJ-**9914",
        "nodes": [
            {"node_id": "n1", "node_type": "goal", "label": "Wire $500K to India property", "value": {"amount": 500000, "destination": "India", "timeline": "Q3 2026"}, "weight": 0.95, "timestamp": "2026-06-01"},
            {"node_id": "n2", "node_type": "behavior", "label": "Typical wires: $25K domestic", "value": {"avg_wire": 25000, "max_wire": 80000, "typical_destination": "domestic", "frequency": "quarterly"}, "weight": 0.88, "timestamp": "2026-05-01"},
            {"node_id": "n3", "node_type": "risk_profile", "label": "Moderate risk tolerance", "value": {"score": 5, "scale": 10, "label": "Moderate"}, "weight": 0.75, "timestamp": "2026-01-15"},
            {"node_id": "n4", "node_type": "portfolio", "label": "AUM $1.8M, liquid $620K", "value": {"aum": 1800000, "liquid": 620000, "target_equity": 60, "actual_equity": 59}, "weight": 0.80, "timestamp": "2026-06-17"},
            {"node_id": "n5", "node_type": "life_event", "label": "International property purchase", "value": {"event": "property_purchase", "country": "India", "amount": 500000}, "weight": 0.90, "timestamp": "2026-06-01"}
        ],
        "edges": [
            {"source": "n1", "target": "n2", "relationship": "ANOMALOUS_VERSUS", "strength": 0.95},
            {"source": "n5", "target": "n1", "relationship": "EXPLAINS", "strength": 0.85},
            {"source": "n4", "target": "n1", "relationship": "FUNDS", "strength": 0.80}
        ]
    }
}
```

---

## 7. BACKEND — core modules

### `/backend/graph/client_graph.py`
Build using NetworkX. Key functions:

```python
def load_client_graph(client_id: str) -> nx.DiGraph:
    """Load client graph from sample data, return NetworkX directed graph."""

def get_context_for_prompt(graph: nx.DiGraph, max_nodes: int = 4) -> dict:
    """
    Traverse graph and extract top-weighted nodes for prompt injection.
    Returns: {
        "context_text": str,       # Formatted for LLM consumption
        "nodes_used": list[dict],  # Which nodes were included
        "key_signals": list[str]   # Plain-English bullet points
    }
    Sort nodes by weight descending, take top max_nodes.
    Format each node as: "[TYPE] {label}: {value}"
    """

def get_graph_for_viz(client_id: str) -> dict:
    """Return graph data formatted for D3 visualization in frontend."""
```

### `/backend/persona/persona_builder.py`
```python
def build_system_prompt(advisor: AdvisorProfile, client_context: dict) -> str:
    """
    Compose the full system prompt by combining:
    1. Static advisor profile fields
    2. Top 2 sample communications (for style reference)
    3. Client context from graph
    
    Returns the full system prompt string.
    Template:
    
    You are an AI assistant helping {advisor.name}, a Raymond James financial advisor.
    
    ADVISOR PROFILE:
    - Name: {advisor.name} | CRD: {advisor.crd} | Branch: {advisor.branch}
    - Specialty: {', '.join(advisor.specialty)}
    - Communication style: {advisor.communication_style}
    - Tone: {advisor.tone}
    - Client base: {advisor.client_demographics}
    - Compliance: {advisor.compliance_scope}
    
    HOW THIS ADVISOR WRITES (examples):
    {sample_1}
    ---
    {sample_2}
    
    CLIENT CONTEXT (from financial memory graph):
    {client_context['context_text']}
    
    INSTRUCTIONS:
    - Write in {advisor.name}'s voice and style exactly as shown in the examples above
    - Reference specific client data from the graph context
    - Keep the tone {advisor.tone}
    - Do not add disclaimers unless the advisor's style includes them
    - Output only the final text, no meta-commentary
    """

def get_persona_summary(advisor: AdvisorProfile) -> dict:
    """Return a simplified dict of which persona fields are being injected, for UI display."""
```

### `/backend/xai/explainer.py`
```python
def compute_shap_attributions(nodes_used: list[dict], recommendation_type: str) -> list[dict]:
    """
    Compute SHAP-style attribution scores for each graph node.
    
    For demo: use weighted scoring based on node weight, edge strength, and
    relationship to the recommendation type.
    
    recommendation_type: "rebalancing" | "wire_review" | "education_funding" | "general"
    
    Returns list of:
    {
        "node_id": str,
        "label": str,
        "node_type": str,
        "shap_value": float,       # Raw SHAP value (-1 to 1)
        "contribution_pct": float,  # % contribution (absolute, sums to 100)
        "direction": "positive" | "negative"  # Whether it supports or opposes the recommendation
    }
    Sorted by abs(shap_value) descending.
    """

def generate_counterfactual(nodes: list[dict], recommendation_type: str) -> str:
    """
    Generate a plain-English counterfactual explanation.
    
    Find the highest-weight node and generate:
    "If [node_label] were [alternative_value], this recommendation would [change_description]."
    
    Examples:
    - "If Margaret's risk tolerance were moderate instead of conservative, 
       rebalancing could wait until Q4 rather than being recommended now."
    - "If Priya's wire pattern included international transfers, 
       this $500K request would not have triggered an AML flag."
    """

def build_xai_result(nodes_used: list[dict], recommendation_type: str) -> XAIResult:
    """Combines shap_attributions + counterfactual + top_drivers + confidence."""
```

### `/backend/llm/claude_client.py`
```python
import anthropic

client = anthropic.Anthropic()

def call_claude(system_prompt: str, user_prompt: str) -> dict:
    """
    Call Claude API with composed system prompt + user prompt.
    Returns: {
        "response": str,
        "tokens_used": int,
        "model": str
    }
    Use: model="claude-sonnet-4-6", max_tokens=1500
    """
```

### `/backend/main.py` — FastAPI routes

```python
# POST /api/prompt
# Request: PromptRequest
# Steps:
#   1. Load advisor profile from ADVISORS[advisor_id]
#   2. Load client graph from CLIENT_GRAPHS[client_id]
#   3. Extract graph context via get_context_for_prompt()
#   4. Build system prompt via build_system_prompt()
#   5. Call Claude via call_claude()
#   6. Compute XAI via build_xai_result()
#   7. Return ApiResponse
# Response: ApiResponse

# GET /api/advisors
# Returns list of all advisors (id, name, crd, branch)

# GET /api/clients
# Returns list of all clients (id, name, account)

# GET /api/graph/{client_id}
# Returns graph data for D3 visualization

# GET /api/advisor/{advisor_id}/persona
# Returns persona summary for display
```

---

## 8. FRONTEND LAYOUT

```
┌─────────────────────────────────────────────────────────────────────┐
│ RJ  Advisor Intelligence Platform        [Persona AI] [XAI] [FINRA] │
├──────────────────┬──────────────────────────────────────────────────┤
│  ADVISOR PANEL   │  CLIENT MEMORY GRAPH           (D3 visualization) │
│                  │                                                    │
│  [Select Adv ▼]  │   [goal]──→[portfolio]──→[behavior]              │
│  Surya Meesala   │      ↘          ↓                                 │
│  CRD: RJ-783...  │      [life_event]──→[risk_profile]               │
│                  │                                                    │
│  Style: Data-1st │  Node colors: goal=gold, risk=navy, event=green  │
│  Tone: Direct    │  Edge thickness = relationship strength           │
│  Spec: Treasury  ├──────────────────────────────────────────────────┤
│                  │  PERSONA INJECTION (collapsible)                  │
│  [Client:     ▼] │  ┌─────────────────────────────────────────────┐ │
│  Margaret Co..   │  │ System prompt being sent to Claude:          │ │
│                  │  │ "You are assisting Surya T. Meesala..."      │ │
│  [Prompt input ] │  │ [advisor profile] + [2 writing samples]      │ │
│  Write Q2        │  │ + [client graph context: 4 nodes]            │ │
│  portfolio rev.. │  └─────────────────────────────────────────────┘ │
│                  ├──────────────────────────────────────────────────┤
│  [⚡ Generate]   │  AI RESPONSE                                      │
│                  │  "Margaret — quick update on your Q2 allocation.  │
│                  │  Your equity drift came in at 8.0%, above your    │
│                  │  7% threshold given your retirement timeline..."   │
│                  ├──────────────────────────────────────────────────┤
│                  │  EXPLAINABILITY (XAI)                             │
│                  │                                                    │
│                  │  WHAT DROVE THIS RECOMMENDATION:                  │
│                  │  Portfolio equity drift  ████████████ 45%         │
│                  │  Retirement timeline     ████████     35%         │
│                  │  Prior rebalancing hist  █████        20%         │
│                  │                                                    │
│                  │  💡 COUNTERFACTUAL:                               │
│                  │  "If Margaret's risk tolerance were moderate,      │
│                  │   rebalancing could wait until Q4."               │
│                  │                                                    │
│                  │  Confidence: 87%  |  FINRA-ready log: ✓           │
└──────────────────┴──────────────────────────────────────────────────┘
```

---

## 9. FRONTEND COMPONENTS

### `AdvisorPanel.jsx`
- Dropdown to select advisor (loads from GET /api/advisors)
- Shows advisor profile: name, CRD, specialty, style, tone
- Dropdown to select client (loads from GET /api/clients)
- Text area for prompt input
- Generate button — calls POST /api/prompt
- Loading state with spinner during API call

### `ClientGraphPanel.jsx`
- D3 force-directed graph visualization
- Loads from GET /api/graph/{client_id} when client changes
- Node colors by type: goal=#FFB81C, risk=#003087, portfolio=#00C46A, behavior=#3B9EFF, life_event=#FF9500, transaction=#7A9BB5
- Node size proportional to weight
- Edge thickness proportional to strength
- Hover tooltip shows node label + value
- Clicking a node highlights it and shows details in sidebar

### `PersonaBuilder.jsx`
- Collapsible panel showing the composed system prompt
- Highlights which sections came from: advisor profile (gold), writing samples (blue), graph context (green)
- Shows count: "Injecting 6 persona fields + 2 writing samples + 4 graph nodes"

### `ResponsePanel.jsx`
- Shows Claude's response with typing animation
- Copy button
- "Send to Client" button (disabled in demo, shows toast)
- Token count display

### `ExplainPanel.jsx`
- Horizontal bar chart (recharts) showing node attributions
- Each bar labeled with node name, colored by node type
- Counterfactual displayed as highlighted callout box
- Confidence score as circular progress
- "FINRA Log Ready ✓" badge — clicking shows the full audit record

---

## 10. RJ DESIGN TOKENS

```javascript
const C = {
  gold:     '#FFB81C',
  navy:     '#003087',
  bg:       '#060C1A',
  card:     '#0C1829',
  cardHi:   '#111F38',
  border:   '#1A304E',
  text:     '#D4E6F6',
  muted:    '#4A7090',
  dim:      '#1A2E44',
  green:    '#00C46A',
  red:      '#FF3B3B',
  blue:     '#3B9EFF',
  orange:   '#FF9500',
}
```

---

## 11. KEY ALGORITHMS IN PLAIN ENGLISH

### Persona Injection (how it works)
```
1. Advisor prompt arrives: "Write Q2 portfolio review email for Margaret"
2. Load AdvisorProfile for this advisor
3. Pick top 2 sample_communications from advisor's history
4. Load ClientGraph for selected client
5. Get top 4 nodes by weight from graph
6. Format as plain text: "Goal: Retire at 65 (4 years). Portfolio: equity drifted +8%. Behavior: accepted 3 prior rebalancings. Life event: spouse retired Jan 2026."
7. Compose system prompt: [static profile] + [2 samples] + [graph context]
8. Send to Claude: system=composed_prompt, user=advisor's raw prompt
9. Claude responds in advisor's voice about this specific client
```

### SHAP Attribution Simulation (for demo)
```
1. After response generated, take nodes_used list
2. For each node, compute attribution score:
   base_score = node.weight
   if node.node_type relates to recommendation_type: multiply by 1.3
   if node has high-strength edges to other nodes: multiply by 1.1
3. Normalize all scores so they sum to 100%
4. Sort descending
5. Top node with highest attribution = primary driver
6. Generate counterfactual based on primary driver
```

### Graph Context Extraction
```
1. Load all nodes for client, sorted by weight descending
2. Take top 4 nodes (configurable)
3. For each node, check its edges — if an edge points to another top node, note the relationship
4. Format as structured text for the prompt:
   "[PORTFOLIO] Equity drift: +8.0% above 7% target
    [GOAL] Retirement at age 65: 4 years remaining
    [BEHAVIOR] Accepted advisor rebalancing 3 times previously
    [LIFE_EVENT] Spouse retired Jan 2026, household income reduced by $45K"
5. Also return nodes_used list for XAI attribution
```

---

## 12. BUILD ORDER

Build in this sequence so each phase is demo-able:

**Phase 1 — Backend skeleton (Day 1)**
- FastAPI app with all routes returning mock data
- Sample data loaded from sample_data.py
- All endpoints returning correct shapes

**Phase 2 — Graph + Persona (Day 1-2)**
- NetworkX graph from sample data
- Context extraction working
- Persona builder composing system prompt
- Claude API call working end-to-end
- Test via curl/Postman first

**Phase 3 — XAI Layer (Day 2)**
- SHAP simulation computing attributions
- Counterfactual generation
- Verify output shapes match ApiResponse

**Phase 4 — Frontend (Day 2-3)**
- React app with Vite
- AdvisorPanel + ClientGraphPanel working
- POST /api/prompt wired up
- Response displaying

**Phase 5 — XAI + Graph Viz (Day 3)**
- D3 graph visualization
- ExplainPanel with recharts bar chart
- PersonaBuilder collapsible panel

**Phase 6 — Polish (Day 4)**
- RJ color tokens applied everywhere
- Loading states, error handling
- Typing animation on response
- Demo script rehearsed

---

## 13. CORS CONFIGURATION

```python
# In main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 14. WHAT MAKES THIS DIFFERENT FROM ALTRUIST HAZEL

| Capability | Hazel (Altruist) | This System |
|---|---|---|
| Data source | RAG over documents | Structured knowledge graph |
| Client intelligence | Document retrieval | Graph traversal + pattern detection |
| Advisor personalization | None | Full persona injection per advisor |
| Explainability | None | SHAP attribution + counterfactual |
| FINRA audit trail | None | Auto-generated per recommendation |
| Wire anomaly detection | None | Graph behavioral baseline comparison |
| Relationship reasoning | Cannot traverse relationships | Native graph edges |

---

## 15. DEMO SCRIPT (for innovation challenge)

1. Open app — show Advisor Surya Meesala selected
2. Select client Margaret Collins — graph loads with 6 nodes
3. Walk through the graph: "This is Margaret's financial memory — her goal, her portfolio drift, her history, her life events — all connected"
4. Expand Persona Builder panel — "Before anything goes to the AI, we inject Surya's persona — his communication style, his voice, his client context"
5. Type prompt: "Write a Q2 portfolio review email for Margaret"
6. Hit Generate — show composed prompt briefly, then response
7. Read response — "Notice it sounds like Surya, not a generic AI. It leads with the 8% number, it's direct, it references her retirement timeline"
8. Show XAI panel — "Here's what drove it: portfolio drift at 45%, retirement timeline at 35%, her behavioral history at 20%"
9. Show counterfactual — "And here's what would have changed the recommendation"
10. "This is what Altruist Hazel cannot do. Hazel retrieves documents. We reason over a connected financial memory. Every output is explainable to a FINRA auditor in 30 seconds."
