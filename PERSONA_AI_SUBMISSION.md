# Persona AI — Submission Content
### RJ MemoryAlpha · Raymond James Engineering Challenge 2026

---

## What Persona AI Does in This System

Before every Claude API call, the system automatically composes:
- **Advisor's profile** (name, CRD, specialty, compliance scope)
- **Advisor's communication style and tone** (data-first vs. relationship-first, etc.)
- **2 actual past emails the advisor wrote** (style reference)
- **Top 4 client graph nodes by weight** (goal, portfolio, behavior, life event)

The advisor types a normal prompt. The enrichment happens in the backend invisibly.
The response comes back sounding like that specific advisor wrote it about that specific client.

---

## Three Points for the Submission

**1. Every AI output already sounds like the advisor wrote it**
The system injects the advisor's actual past emails as style examples before calling
the AI. The draft that comes back does not need to be rewritten — it leads the way
Surya leads, uses the words Jennifer uses. The advisor reviews and approves;
they do not redraft.

**2. No two advisors produce the same output**
Generic AI tools give every advisor the same voice. This system produces a different
output for every advisor even with the same client data and the same prompt. That
differentiation is built from their own writing history, not a configuration setting.

**3. The persona enrichment is invisible to the advisor**
The advisor types a normal prompt. The enrichment happens automatically in the backend
before the API call. The advisor does not fill out a style form or toggle settings.
It just works, every time.

---

## Where to Place Each Point in the Submission Portal

### Business Problem — add this sentence after the existing bullet list:
> "Even when advisors know what to say, drafting personalized communications at scale
> takes time they do not have. Generic AI output — one voice for all advisors, all
> clients — erodes the relationship trust that took years to build."

### Proposed Idea — add after the existing graph node + context-aware intelligence section:
> "A Persona AI layer sits between the advisor's prompt and the AI model. Before
> every call, the system automatically injects the advisor's communication style,
> tone, and two examples of how they actually write — alongside the client's graph
> context. The response comes back in that advisor's specific voice about that
> specific client. Surya's output leads with numbers and is direct. Jennifer's is
> warm and relationship-first. Same prompt. Same client data. Completely different
> voice — because the system learned from their actual past writing."

### Relevance to the Firm — For Advisors section, add:
> "Every AI draft arrives in the advisor's own voice — reducing the time spent
> rewriting generic AI output into something that sounds like them."

### Relevance to the Firm — For the Firm section, add:
> "Operationalizes the 'power of personal' strategy as a technology capability,
> not just a cultural aspiration. Captures each advisor's communication style in
> a structured, portable form that persists and improves over time — every
> communication the advisor approves becomes a new training example that sharpens
> the persona, and that knowledge persists beyond individual personnel changes."

### Implementation — Phase 3 (AI Integration), add bullet:
> "Deploy Persona AI layer: advisor profile + writing sample injection + client
> graph context composition before every LLM call. The advisor profile is not
> static — it updates continuously as the advisor approves and sends communications,
> so the persona sharpens over time from their own usage. Human-in-the-loop:
> advisor reviews every draft before it reaches the client."

### Risks — add new risk block:
> **AI Output Quality — Persona Drift**
> - Risk: AI draft does not accurately reflect the advisor's voice or contains
>   tone inconsistencies the advisor would not use
> - Mitigation: Advisor review required before any communication is sent.
>   Writing samples are sourced directly from the advisor's own past emails.
>   The composed system prompt is stored per output and can be audited.

---

## Technical Reference

Few-shot prompting — the mechanism behind persona injection:
Brown et al., "Language Models are Few-Shot Learners," NeurIPS 2020
https://arxiv.org/abs/2005.14165

FINRA AI governance guidance:
FINRA Regulatory Notice 24-09, 2024
https://www.finra.org/rules-guidance/notices/24-09
