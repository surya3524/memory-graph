const BASE = "http://localhost:8000";

export const getAdvisors  = () => fetch(`${BASE}/api/advisors`).then(r => r.json());
export const getClients   = () => fetch(`${BASE}/api/clients`).then(r => r.json());
export const getGraph     = (clientId) => fetch(`${BASE}/api/graph/${clientId}`).then(r => r.json());
export const getPersona   = (advisorId) => fetch(`${BASE}/api/advisor/${advisorId}/persona`).then(r => r.json());

export const runPrompt = (advisorId, clientId, userPrompt) =>
  fetch(`${BASE}/api/prompt`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ advisor_id: advisorId, client_id: clientId, user_prompt: userPrompt })
  }).then(r => r.json());
