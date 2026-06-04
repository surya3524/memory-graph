"""
Meeting Note Encoder — uses Claude API to extract graph nodes and edges
from raw advisor meeting notes.
"""

import os
import json
import anthropic

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a financial advisor intelligence system.
Your job is to extract structured memory graph data from raw advisor meeting notes.

Extract ONLY what the client explicitly stated or did — never infer or assume.

Return a JSON object with this exact structure:
{
  "nodes": [
    {"type": "belief|emotion|action|event", "label": "snake_case_label", "summary": "one sentence"}
  ],
  "edges": [
    {"from": "label_of_source_node", "relation": "RELATION_TYPE", "to": "label_of_target_node"}
  ],
  "advisor_alert": {
    "action": "CALL FIRST|CALL THIS WEEK|EMAIL TODAY|GENTLE CHECK-IN|MONITOR",
    "trigger": "what market condition would activate this",
    "context": "why this client needs attention when trigger fires",
    "suggested_approach": "what the advisor should say or do"
  }
}

Valid node types:
- belief: something the client stated they believe
- emotion: how the client felt or reacted to a situation
- action: something the client did with their portfolio
- event: a market or life event referenced

Valid edge relation types:
TRIGGERED_BY, LED_TO, REFLECTS_ON, REINFORCES, EVOLVED_FROM,
SHAPED_BY, DRIVEN_BY, TENSION_WITH, INFLUENCED_BY, CONNECTED_TO

Rules:
- Labels must be snake_case, under 5 words, descriptive
- Only create edges between nodes you defined in this response
- If something is ambiguous, omit it rather than guess
- Return only valid JSON, no explanation text"""


def encode_meeting_note(client_name: str, meeting_date: str, raw_note: str) -> dict:
    prompt = f"""Client: {client_name}
Meeting date: {meeting_date}

Advisor meeting notes:
{raw_note}

Extract the graph nodes, edges, and advisor alert from these notes."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def print_encoded(client_name: str, date: str, note: str):
    print(f"\n{'━' * 60}")
    print(f"  Client: {client_name}  |  Date: {date}")
    print(f"{'━' * 60}")
    print(f"  Note: {note[:120]}{'...' if len(note) > 120 else ''}\n")

    result = encode_meeting_note(client_name, date, note)

    print("  NODES extracted:")
    for n in result.get("nodes", []):
        print(f"    [{n['type'].upper():8}] {n['label']}")
        print(f"             → {n['summary']}")

    print("\n  EDGES extracted:")
    for e in result.get("edges", []):
        print(f"    {e['from']}  —{e['relation']}→  {e['to']}")

    alert = result.get("advisor_alert", {})
    if alert:
        print(f"\n  ADVISOR ALERT:")
        print(f"    Action  : {alert.get('action')}")
        print(f"    Trigger : {alert.get('trigger')}")
        print(f"    Context : {alert.get('context')}")
        print(f"    Approach: {alert.get('suggested_approach')}")

    return result


if __name__ == "__main__":
    sample_note = (
        "Client called today very concerned about the market drop. "
        "Said he's been watching CNBC all morning and is thinking about moving "
        "to cash. Reminded him of his 2020 experience. He paused and said "
        "'You're right, I did this before and regretted it.' "
        "Agreed to hold for now but wants a call if it drops another 3%."
    )

    print_encoded("John M.", "2025-06-02", sample_note)
