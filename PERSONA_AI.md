# Persona AI — Advantages, Business Value & Integration Guide
### RJ MemoryAlpha · Raymond James Engineering Challenge 2026

---

## What Persona AI Does

The system automatically composes this before every Claude API call:

```
[Advisor's name, CRD, branch, specialty]
+ [Advisor's communication style + tone]
+ [2 actual past emails that advisor wrote]
+ [Client's graph context: top 4 nodes by weight]
+ [Advisor's raw prompt]
→ Claude responds in that advisor's specific voice about that specific client
```

The result: Surya's output leads with numbers, is direct, skips filler phrases.
Jennifer's output is warm, story-driven, relationship-first.
Same prompt. Same client data. Completely different voice.
Because the system learned from their actual past writing.

---

## How It Is Built (from the spec)

### AdvisorProfile data model
```python
class AdvisorProfile(BaseModel):
    advisor_id: str
    name: str                          # "Surya T. Meesala"
    crd: str                           # "RJ-7832104"
    branch: str                        # "Las Cruces, NM"
    specialty: list[str]               # ["Treasury Wires", "HNW clients", "Retirement Planning"]
    communication_style: str           # "data-first, concise, leads with key numbers"
    tone: str                          # "direct and professional, avoids filler phrases"
    client_demographics: str           # "Ages 45-68, $1M-$5M AUM"
    relationship_style: str            # "proactive outreach, weekly for top-tier clients"
    compliance_scope: str              # "New Mexico registered, no discretionary authority"
    sample_communications: list[str]   # Actual past emails the advisor wrote
```

### What gets composed as the system prompt
```
You are an AI assistant helping {advisor.name}, a Raymond James financial advisor.

ADVISOR PROFILE:
- Specialty: {advisor.specialty}
- Communication style: {advisor.communication_style}
- Tone: {advisor.tone}
- Compliance: {advisor.compliance_scope}

HOW THIS ADVISOR WRITES (examples):
{sample_email_1}
---
{sample_email_2}

CLIENT CONTEXT (from financial memory graph):
[PORTFOLIO] Equity drift: +8.0% above 7% target
[GOAL] Retirement at age 65: 4 years remaining
[BEHAVIOR] Accepted advisor rebalancing 3 times previously
[LIFE_EVENT] Spouse retired Jan 2026, household income reduced by $45K

INSTRUCTIONS:
- Write in {advisor.name}'s voice exactly as shown in the examples above
- Reference specific client data from the graph context
- Keep the tone {advisor.tone}
- Output only the final text, no meta-commentary
```

---

## Advantages — Framed for C-Level Judges

### 1. Every AI output already sounds like the advisor wrote it
The system injects the advisor's actual past emails as style examples before calling
the AI. The draft that comes back does not need to be rewritten — it leads the way
Surya leads, uses the words Jennifer uses. The advisor reviews and approves,
they do not redraft.

### 2. No two advisors produce the same output
Generic AI tools — including adding an AI assistant to a CRM — give every advisor
the same voice. This system produces a different output for every advisor even with
the same client data and the same prompt. That differentiation is built from their
own writing history, not a configuration setting.

### 3. The persona enrichment is invisible to the advisor
The advisor types a normal prompt. The enrichment happens automatically in the
backend before the API call. The advisor does not fill out a style form or toggle
settings. It just works, every time.

### 4. Compliance can read and audit the exact instructions given to the AI
The composed system prompt is stored with every output. It is plain text — not a
black box model weight. A compliance officer can open the log for any AI-assisted
communication and read word-for-word what the system told the AI before it generated
the response. This is auditable in a way that fine-tuned models are not.

Relevant regulation: FINRA Notice 24-09 on AI governance (2024)
Verify at: https://www.finra.org/rules-guidance/notices/24-09

### 5. Scales advisor capacity without scaling headcount
An advisor managing 200 clients who previously spent time drafting a personal email
now spends a fraction of that time reviewing an AI draft. The time-per-communication
reduction across thousands of RJ advisors is the metric to measure in the pilot.
*(No specific dollar figure claimed — this is the measurable outcome for the pilot.)*

### 6. Supports the "power of personal" strategy with a technical mechanism
The CEO stated the firm's differentiator is deeply personal relationships. Persona AI
is the first technology implementation that operationalizes that statement — every
AI-assisted communication reflects the specific advisor's voice, not a generic firm voice.

Paul Shoukry, CNBC interview, Nov 12, 2025:
Verify at: https://www.cnbc.com — search "Paul Shoukry Raymond James 2025"

---

## What This Is Not

- It does not fine-tune or retrain a model on advisor data
- It does not store client PII in a third-party vector database in production
  (ChromaDB is used for demo only — production would use an RJ-hosted vector store)
- It does not make suitability determinations — every output requires advisor review
  before any client action

---

## Where This Fits in the Submission Sections

| Section | What to add |
|---|---|
| **Business Problem** | "Even when advisors know what to say, drafting personalized communications at scale takes time they do not have. Generic AI output erodes the relationship trust that took years to build." |
| **Proposed Idea** | After browser agent paragraph: introduce Persona AI as the third capability — the output layer that makes every AI draft sound like the advisor wrote it |
| **Relevance → For the Firm** | "Operationalizes the 'power of personal' strategy as a technology capability, not just a cultural aspiration" |
| **Relevance → For the Firm** | "Captures advisor communication style in a structured, portable form that persists beyond individual personnel changes" |
| **Implementation → Phase 3** | Replace generic AI integration bullets with: Persona AI layer deployment + XAI layer deployment + FINRA audit log per output |
| **Risks** | New block: AI Output Quality — mitigation is advisor review required before sending + full composed prompt stored per output |
| **Pilot Proposal** | Add fourth metric: reduction in time to first draft per client communication |

---

## Technical References

1. Few-shot prompting — the mechanism behind persona injection
   Brown et al., "Language Models are Few-Shot Learners," NeurIPS 2020
   https://arxiv.org/abs/2005.14165

2. SHAP — the explainability method used in the XAI layer
   Lundberg & Lee, "A Unified Approach to Interpreting Model Predictions," NeurIPS 2017
   https://arxiv.org/abs/1705.07874

3. Counterfactual explanations
   Wachter, Mittelstadt, Russell, Harvard JOLT 2017
   https://arxiv.org/abs/1711.00399

4. FINRA AI governance guidance
   FINRA Regulatory Notice 24-09, 2024
   https://www.finra.org/rules-guidance/notices/24-09

5. Vanguard Advisor's Alpha — behavioral coaching adds ~150bps annually
   Kinniry et al., Vanguard 2022
   https://workplace.vanguard.com/content/dam/inst/iig-transformation/insights/pdf/2022/advisor-alpha-quantifying-the-value-of-a-financial-professional.pdf

6. DALBAR QAIB — behavioral gap in investor returns
   DALBAR 30th Annual Edition, April 2024
   https://www.dalbar.com/qaib/

---

*All claims in this document are sourced. Verify each link before including in the
final submission. Do not add claims that cannot be independently verified.*
