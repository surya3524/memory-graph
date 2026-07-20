import { useState, useEffect } from "react";
import { getAdvisors, getClients } from "./api/client";
import AdvisorPanel from "./components/AdvisorPanel";
import ClientGraphPanel from "./components/ClientGraphPanel";
import PersonaBuilder from "./components/PersonaBuilder";
import ResponsePanel from "./components/ResponsePanel";
import ExplainPanel from "./components/ExplainPanel";

const S = {
  app: { display: "flex", flexDirection: "column", minHeight: "100vh" },
  header: {
    background: "var(--navy)", borderBottom: "2px solid var(--gold)",
    padding: "12px 24px", display: "flex", alignItems: "center", gap: 16
  },
  logo: { color: "var(--gold)", fontWeight: 800, fontSize: 18, letterSpacing: 1 },
  sub: { color: "var(--text)", fontSize: 12, opacity: 0.7 },
  badges: { marginLeft: "auto", display: "flex", gap: 8 },
  badge: {
    background: "var(--cardHi)", border: "1px solid var(--border)",
    borderRadius: 20, padding: "4px 12px", fontSize: 11, color: "var(--gold)"
  },
  body: { display: "flex", flex: 1, overflow: "hidden" },
  left: { width: 300, borderRight: "1px solid var(--border)", overflowY: "auto", flexShrink: 0 },
  right: { flex: 1, display: "flex", flexDirection: "column", overflowY: "auto" },
  top: { display: "flex", flex: 1, borderBottom: "1px solid var(--border)" },
  graphWrap: { flex: 1, borderRight: "1px solid var(--border)" },
  bottom: { display: "flex", minHeight: 280 },
  responseWrap: { flex: 1, borderRight: "1px solid var(--border)" },
};

export default function App() {
  const [advisors, setAdvisors] = useState([]);
  const [clients, setClients]   = useState([]);
  const [advisorId, setAdvisorId] = useState("ADV001");
  const [clientId, setClientId]   = useState("C001");
  const [result, setResult]       = useState(null);
  const [loading, setLoading]     = useState(false);

  useEffect(() => {
    getAdvisors().then(setAdvisors).catch(() => {});
    getClients().then(setClients).catch(() => {});
  }, []);

  return (
    <div style={S.app}>
      <header style={S.header}>
        <div>
          <div style={S.logo}>RJ  Advisor Intelligence Platform</div>
          <div style={S.sub}>Persona AI · Explainable AI · Client Memory Graph</div>
        </div>
        <div style={S.badges}>
          <span style={S.badge}>Persona AI</span>
          <span style={S.badge}>XAI</span>
          <span style={S.badge}>FINRA-ready</span>
        </div>
      </header>

      <div style={S.body}>
        <div style={S.left}>
          <AdvisorPanel
            advisors={advisors} clients={clients}
            advisorId={advisorId} clientId={clientId}
            onAdvisor={setAdvisorId} onClient={setClientId}
            onResult={setResult} onLoading={setLoading}
            loading={loading}
          />
        </div>

        <div style={S.right}>
          <div style={S.top}>
            <div style={S.graphWrap}>
              <ClientGraphPanel clientId={clientId} />
            </div>
            <PersonaBuilder advisorId={advisorId} result={result} />
          </div>

          <div style={S.bottom}>
            <div style={S.responseWrap}>
              <ResponsePanel result={result} loading={loading} />
            </div>
            <ExplainPanel result={result} />
          </div>
        </div>
      </div>
    </div>
  );
}
