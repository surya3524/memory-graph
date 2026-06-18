# Explainable AI (XAI) — Submission Content
### RJ MemoryAlpha · Raymond James Engineering Challenge 2026

---

## What XAI Does in This System

Every AI-generated recommendation surfaces:
- **Which graph nodes drove it** (SHAP-style attribution with % contribution)
- **What would have changed the outcome** (counterfactual in plain English)
- **A full compliance log** stored at the point of generation

---

## Three Points for the Submission

**1. The advisor can see exactly why the AI said what it said**
After every generated response, the XAI panel shows a bar chart of which graph nodes
drove the recommendation — portfolio drift, retirement timeline, behavioral history —
each with a percentage contribution. The advisor isn't trusting a black box. They're
seeing "45% of this recommendation came from her equity drift being 8% above target."
That's a fact they can verify, explain to the client, and defend to a manager.

**2. The counterfactual tells the advisor what would change the outcome**
For every recommendation, the system generates one plain-English counterfactual:
"If Margaret's risk tolerance were moderate instead of conservative, the rebalance
could wait until Q4." This tells the advisor which variable matters most — so if the
client pushes back, the advisor knows exactly which fact to address rather than
re-explaining the whole recommendation.

**3. Every recommendation auto-generates a compliance log at the point of generation**
The composed system prompt, the graph nodes used, the SHAP attribution scores, and the
counterfactual are all stored together as a single record tied to that recommendation.
If compliance asks six months later "why did the AI suggest this rebalance to Margaret
in June?" — the answer is already in the log. Nothing needs to be reconstructed
from memory.

---

## Where to Place Each Point in the Submission Portal

### Business Problem — add this paragraph after the existing bullet list:
> "Current AI tools in wealth management generate recommendations without explaining
> them. Advisors cannot tell a client — or a compliance officer — which facts drove
> the AI's output. As AI-assisted advice scales, this opacity becomes a regulatory
> and trust risk. There is no structured mechanism today to make AI recommendations
> auditable at the moment they are generated."

### Proposed Idea — add after the existing graph node descriptions:
> "A built-in Explainability layer (XAI) accompanies every AI output. The advisor
> sees a breakdown of which client memory nodes drove the recommendation and a
> plain-English counterfactual showing what would have changed it. This makes
> every AI-assisted output defensible to the client, to the advisor's manager,
> and to a compliance review."

### Relevance to the Firm — For Advisors section, add:
> "Shows the advisor why the AI said what it said, so they can explain it to the
> client in their own words — not just read an AI output they cannot defend."

### Relevance to the Firm — For the Firm section, add:
> "Auto-generates a FINRA-ready audit log per AI recommendation at the point of
> generation. Compliance cost shifts from reactive (reconstruct the reasoning after
> a complaint) to zero (log already exists)."
> Reference: FINRA Regulatory Notice 24-09 — https://www.finra.org/rules-guidance/notices/24-09

### Implementation — Phase 3 (AI Integration), add bullet:
> "Deploy XAI layer: SHAP-style node attribution + counterfactual generation +
> per-recommendation compliance log stored with full prompt and graph context used."

### Risks — add new risk block after Data Accuracy & Integrity:
> **AI Output Quality**
> - Risk: AI generates a recommendation the advisor cannot explain or defend
> - Mitigation: Advisor review required before any client action. XAI panel shows
>   which graph nodes drove the output so the advisor can validate the reasoning
>   before approving. Full attribution log stored per output.
