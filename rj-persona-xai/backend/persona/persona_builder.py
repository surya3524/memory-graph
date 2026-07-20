from persona.persona_store import get_advisor

def build_system_prompt(advisor_id: str, client_context: dict) -> str:
    advisor = get_advisor(advisor_id)
    samples = advisor["sample_communications"]
    sample_1 = samples[0] if len(samples) > 0 else ""
    sample_2 = samples[1] if len(samples) > 1 else ""

    return f"""You are an AI assistant helping {advisor['name']}, a Raymond James financial advisor.

ADVISOR PROFILE:
- Name: {advisor['name']} | CRD: {advisor['crd']} | Branch: {advisor['branch']}
- Specialty: {', '.join(advisor['specialty'])}
- Communication style: {advisor['communication_style']}
- Tone: {advisor['tone']}
- Client base: {advisor['client_demographics']}
- Compliance: {advisor['compliance_scope']}

HOW THIS ADVISOR WRITES (examples):
{sample_1}
---
{sample_2}

CLIENT CONTEXT (from financial memory graph):
{client_context['context_text']}

INSTRUCTIONS:
- Write in {advisor['name']}'s voice and style exactly as shown in the examples above
- Reference specific client data from the graph context above
- Keep the tone: {advisor['tone']}
- Do not add disclaimers unless the advisor's style includes them
- Do not make suitability determinations — the advisor will review before sending
- Output only the final text, no meta-commentary"""

def get_persona_summary(advisor_id: str) -> dict:
    advisor = get_advisor(advisor_id)
    return {
        "name": advisor["name"],
        "style": advisor["communication_style"],
        "tone": advisor["tone"],
        "specialty": advisor["specialty"],
        "samples_count": len(advisor["sample_communications"]),
        "fields_injected": 6
    }
