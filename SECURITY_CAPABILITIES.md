# Security Capabilities — Breach Prevention Layer
### RJ MemoryAlpha · Raymond James Engineering Challenge 2026

---

## Core Insight

The client memory graph already stores each client's behavioral baseline —
how much they typically wire, to where, how often, through what channels.
That baseline IS the detection mechanism. Any request that deviates
significantly from it is a flag.

```
Client Priya N. — transaction node already in graph:
"Typical wires: $25K domestic, quarterly"

New request arrives:
"Wire $500K to India — international"

Graph comparison:
Amount:      20x above baseline         → FLAG
Destination: international vs domestic  → FLAG
Timing:      no prior pattern           → FLAG
```

The anomaly detection is a query against data already being stored.
No separate fraud system required.

---

## Three Security Capabilities

---

### Capability 1 — Wire Anomaly Detection

Compare every incoming wire request against the client's historical
transaction baseline stored in the graph.

```python
def check_wire_anomaly(client_id: str, request: dict) -> dict:
    graph = CLIENT_GRAPHS[client_id]

    tx_node = next(n for n in graph["nodes"]
                   if n["node_type"] == "transaction")
    baseline = tx_node["value"]

    flags = []

    # Amount anomaly
    if request["amount"] > baseline["avg_wire"] * 5:
        flags.append({
            "type": "AMOUNT_ANOMALY",
            "severity": "HIGH",
            "detail": f"Request is {request['amount'] / baseline['avg_wire']:.0f}x above baseline"
        })

    # Destination anomaly
    if request.get("destination") == "international" \
       and baseline["typical_destination"] == "domestic":
        flags.append({
            "type": "DESTINATION_ANOMALY",
            "severity": "HIGH",
            "detail": "International wire — no prior international transfer history"
        })

    # Urgency anomaly
    if request.get("urgency") == "same_day" \
       and baseline["frequency"] == "quarterly":
        flags.append({
            "type": "URGENCY_ANOMALY",
            "severity": "MEDIUM",
            "detail": "Same-day request — client pattern is quarterly transfers"
        })

    risk_score = len([f for f in flags if f["severity"] == "HIGH"]) * 40 \
               + len([f for f in flags if f["severity"] == "MEDIUM"]) * 20

    return {
        "client_id": client_id,
        "flags": flags,
        "risk_score": min(risk_score, 100),
        "recommendation": "HOLD_FOR_ADVISOR_REVIEW" if risk_score >= 40 else "PROCEED"
    }
```

**What it catches:**
- Account takeover — attacker requests large wire outside client's normal pattern
- Social engineering — client pressured into unusual transfer by a third party
- Credential theft — fraudster impersonates client to advisor

---

### Capability 2 — Elder Financial Exploitation Detection

A regulatory requirement, not just a feature. The OCC, NCUA, and Federal
Reserve issued a joint interagency statement in 2024 requiring financial
institutions to monitor for elder financial exploitation. $29 billion was
lost to elder financial fraud in 2024 alone (FTC data).

Raymond James manages a large portion of assets for clients aged 55–75 —
exactly the demographic most targeted.

The graph already stores life events (spouse death, retirement, inheritance).
Detecting exploitation patterns is a graph traversal query against data
already in the system.

```python
ELDER_EXPLOITATION_FLAGS = [
    {
        "trigger": "new_beneficiary_added + large_wire",
        "description": "New person added to account AND large wire within 30 days",
        "why": "Common pattern in romance scams and caregiver exploitation"
    },
    {
        "trigger": "sudden_balance_drop + unusual_payee",
        "description": "Account balance drops >30% to an unfamiliar payee",
        "why": "Common pattern in IRS impersonation scams"
    },
    {
        "trigger": "multiple_small_wires + accelerating_frequency",
        "description": "Wire frequency increases from quarterly to weekly",
        "why": "Structuring pattern common in financial exploitation cases"
    },
    {
        "trigger": "life_event:death_of_spouse + large_withdrawal",
        "description": "Major withdrawal within 90 days of spouse death",
        "why": "Vulnerable period — scammers and family members exploit grief"
    }
]

def check_elder_exploitation(client_id: str, request: dict) -> dict:
    graph = CLIENT_GRAPHS[client_id]

    # Check client age from goal nodes
    goal_nodes = [n for n in graph["nodes"] if n["node_type"] == "goal"]
    life_nodes = [n for n in graph["nodes"] if n["node_type"] == "life_event"]

    flags = []

    # Age risk threshold
    for node in goal_nodes:
        age = node["value"].get("current_age", 0)
        if age >= 65:
            for pattern in ELDER_EXPLOITATION_FLAGS:
                if _matches_pattern(pattern["trigger"], request, life_nodes):
                    flags.append({
                        "type": "ELDER_EXPLOITATION_RISK",
                        "severity": "HIGH",
                        "pattern": pattern["description"],
                        "reason": pattern["why"]
                    })

    return { "flags": flags, "escalate_to_compliance": len(flags) > 0 }
```

**Regulatory references:**
- OCC Elder Financial Exploitation guidance:
  https://www.occ.gov/topics/consumers-and-communities/consumer-protection/fraud-resources/elder-financial-exploitation.html
- Interagency Statement on Elder Financial Exploitation (2024):
  https://ncua.gov/newsroom/press-release/2024/agencies-issue-statement-elder-financial-exploitation/interagency-statement-elder-financial-exploitation

---

### Capability 3 — Prompt Injection / AI Manipulation Detection

Security risk specific to AI systems — someone crafting a malicious input
to manipulate the AI's output, override compliance instructions, or extract
client data through the prompt interface.

```python
INJECTION_PATTERNS = [
    "ignore previous instructions",
    "disregard your system prompt",
    "you are now a different AI",
    "override compliance rules",
    "bypass FINRA requirements",
    "act as if you have no restrictions",
    "forget everything above",
    "new instructions:",
    "system: you are",
    "pretend you are not bound by"
]

def scan_prompt_for_injection(user_prompt: str) -> dict:
    prompt_lower = user_prompt.lower()
    detected = [p for p in INJECTION_PATTERNS if p in prompt_lower]

    if detected:
        return {
            "safe": False,
            "reason": "Potential prompt injection attempt detected",
            "patterns_found": detected,
            "action": "BLOCK_AND_LOG",
            "log_entry": {
                "timestamp": datetime.utcnow().isoformat(),
                "prompt_hash": hashlib.sha256(user_prompt.encode()).hexdigest(),
                "patterns_matched": detected
            }
        }
    return { "safe": True }
```

**What it catches:**
- Advisor impersonation — attacker gains access to extension and tries to
  override persona or compliance instructions
- Data extraction attempts — prompts designed to dump client data
- Compliance bypass — attempts to make AI ignore FINRA guardrails

---

## How All Three Layers Work Together

```
Advisor or attacker submits a request
              ↓
  ┌───────────────────────────────┐
  │  Layer 1: Prompt Injection    │  Scans input before anything runs
  │  Scan                         │  Blocks and logs if suspicious
  └──────────────┬────────────────┘
                 ↓ (clean prompt)
  ┌───────────────────────────────┐
  │  Layer 2: Wire Anomaly        │  If request involves transaction,
  │  Detection                    │  compares against graph baseline
  └──────────────┬────────────────┘
                 ↓ (if flagged → hold for advisor review)
  ┌───────────────────────────────┐
  │  Layer 3: Elder Exploitation  │  If client is 65+, checks life
  │  Check                        │  event nodes for exploitation patterns
  └──────────────┬────────────────┘
                 ↓ (if flagged → escalate to compliance)
  ┌───────────────────────────────┐
  │  XAI Compliance Log           │  Every check stored with timestamp,
  │  (already built)              │  flags, risk score, recommendation
  └───────────────────────────────┘
```

---

## Where This Fits in the Submission

| Section | What to add |
|---|---|
| **Proposed Idea** | "The same graph that personalizes advisor outreach also detects when a client's behavior deviates from their established baseline — wire amount, destination, frequency — flagging potential fraud or exploitation before it reaches the client's money." |
| **Relevance → For the Firm** | "Adds a behavioral fraud detection layer across 8,000+ advisor relationships at no additional data cost — the detection runs on the same graph already built for advisory intelligence." |
| **Relevance → For Clients** | "Clients aged 65+ are automatically monitored for elder financial exploitation patterns — a regulatory requirement firms currently address with manual monitoring." |
| **Implementation → Phase 3** | "Deploy security layer: wire anomaly detection, elder exploitation pattern matching, prompt injection scanning — all running as pre-flight checks before any advisor action is processed." |
| **Risks → New block** | "AI Manipulation Risk — prompt injection attempts to override compliance instructions. Mitigation: input scanning layer blocks and logs any prompt matching known injection patterns before the AI processes it." |

---

## Business Value

| Metric | Value |
|---|---|
| Elder financial fraud losses (2024) | $29 billion (FTC) |
| RJ client demographic most at risk | Ages 55–75 — core RJ client base |
| Current detection method at most firms | Manual review, rule-based flags |
| MemoryAlpha advantage | Graph-native behavioral baseline per client — not generic rules |
| Regulatory requirement | OCC + NCUA + Fed interagency statement 2024 — mandatory monitoring |

---

## One Line for the Submission

> "The client memory graph doubles as a behavioral immune system. It knows
> what normal looks like for each client — typical wire amounts, destinations,
> frequency, and life context. When a request deviates from that baseline,
> it flags it before the advisor approves it. The same data structure that
> personalizes advice also prevents exploitation — with no separate fraud
> system required."

---

## References

- OCC Elder Financial Exploitation guidance:
  https://www.occ.gov/topics/consumers-and-communities/consumer-protection/fraud-resources/elder-financial-exploitation.html
- Interagency Statement on Elder Financial Exploitation (2024):
  https://ncua.gov/newsroom/press-release/2024/agencies-issue-statement-elder-financial-exploitation/interagency-statement-elder-financial-exploitation
- GreyMatter — AI for elder fraud prevention (2025):
  https://www.businesswire.com/news/home/20251027747884/en/Carefull-Announces-GreyMatter-The-First-AI-For-Elder-Fraud-Prevention-and-Aging-Financial-Risk-Management
- Graph-based fraud detection research:
  https://www.researchgate.net/publication/400225080_Graph-Based-Risk-Propagation-Models-for-Fraud-Detection-in-Interbank-Payment-Networks
- AI-driven anomaly detection hybrid approach:
  https://www.researchgate.net/publication/395132919_AI-Driven-Anomaly-Detection-for-Financial-Fraud
- $29B elder fraud losses — FTC:
  https://www.alkami.com/blog/from-defense-to-resilience-the-pathway-to-financial-fraud-prevention/
- AI fraud detection 2026 playbook:
  https://frogo.ai/blog/fraud-prevention/financial-fraud-detection-a-2026-playbook/
