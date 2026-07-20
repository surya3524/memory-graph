import os
import anthropic

_client = None

def get_client():
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _client

def call_claude(system_prompt: str, user_prompt: str) -> dict:
    client = get_client()
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}]
    )
    return {
        "response": response.content[0].text,
        "tokens_used": response.usage.input_tokens + response.usage.output_tokens,
        "model": response.model
    }
