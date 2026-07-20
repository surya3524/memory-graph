import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from graph.client_graph import get_context_for_prompt, get_graph_for_viz
from graph.sample_data import CLIENT_GRAPHS
from persona.persona_builder import build_system_prompt, get_persona_summary
from persona.persona_store import list_advisors
from xai.explainer import build_xai_result
from llm.claude_client import call_claude

app = FastAPI(title="RJ Persona XAI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    advisor_id: str
    client_id: str
    user_prompt: str

@app.get("/api/advisors")
def get_advisors():
    return list_advisors()

@app.get("/api/clients")
def get_clients():
    return [
        {"client_id": c["client_id"], "client_name": c["client_name"], "account": c["account"]}
        for c in CLIENT_GRAPHS.values()
    ]

@app.get("/api/graph/{client_id}")
def get_graph(client_id: str):
    if client_id not in CLIENT_GRAPHS:
        raise HTTPException(status_code=404, detail="Client not found")
    return get_graph_for_viz(client_id)

@app.get("/api/advisor/{advisor_id}/persona")
def get_persona(advisor_id: str):
    try:
        return get_persona_summary(advisor_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/api/prompt")
def run_prompt(req: PromptRequest):
    try:
        # 1. Extract graph context
        client_context = get_context_for_prompt(req.client_id)

        # 2. Build persona system prompt
        system_prompt = build_system_prompt(req.advisor_id, client_context)

        # 3. Call Claude
        llm_result = call_claude(system_prompt, req.user_prompt)

        # 4. Compute XAI
        xai_result = build_xai_result(client_context["nodes_used"], req.user_prompt)

        # 5. Persona summary for UI
        persona_injected = get_persona_summary(req.advisor_id)

        return {
            "composed_prompt": system_prompt,
            "persona_injected": persona_injected,
            "graph_context_used": client_context["key_signals"],
            "llm_response": llm_result["response"],
            "xai_result": xai_result,
            "tokens_used": llm_result["tokens_used"]
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
