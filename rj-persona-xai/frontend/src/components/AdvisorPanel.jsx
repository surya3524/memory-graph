import { useState } from "react";
import { runPrompt } from "../api/client";

const S = {
  wrap: { padding: 16, display: "flex", flexDirection: "column", gap: 16 },
  section: { display: "flex", flexDirection: "column", gap: 6 },
  label: { fontSize: 11, color: "var(--muted)", textTransform: "uppercase", letterSpacing: 1 },
  select: {
    background: "var(--cardHi)", border: "1px solid var(--border)",
    color: "var(--text)", borderRadius: 6, padding: "8px 10px", width: "100%", fontSize: 13
  },
  chip: {
    display: "inline-block", background: "var(--card)", border: "1px solid var(--border)",
    borderRadius: 4, padding: "2px 8px", fontSize: 11, color: "var(--gold)", marginRight: 4, marginBottom: 4
  },
  infoRow: { display: "flex", justifyContent: "space-between", fontSize: 12 },
  infoVal: { color: "var(--text)" },
  infoKey: { color: "var(--muted)" },
  textarea: {
    background: "var(--cardHi)", border: "1px solid var(--border)",
    color: "var(--text)", borderRadius: 6, padding: "10px", width: "100%",
    fontSize: 13, resize: "vertical", minHeight: 90, fontFamily: "inherit"
  },
  btn: {
    background: "var(--gold)", color: "#000", border: "none",
    borderRadius: 6, padding: "10px 0", width: "100%",
    fontWeight: 700, fontSize: 14, cursor: "pointer", letterSpacing: 0.5
  },
  btnLoading: { background: "var(--muted)", cursor: "not-allowed" },
  divider: { borderTop: "1px solid var(--border)" },
  title: { fontSize: 13, fontWeight: 600, color: "var(--gold)", marginBottom: 4 }
};

const ADVISOR_META = {
  ADV001: { style: "Data-first, concise", tone: "Direct & professional", spec: "Treasury · HNW · Retirement" },
  ADV002: { style: "Relationship-first, warm", tone: "Conversational, empathetic", spec: "Estate · Business Owners" }
};

const PROMPTS = [
  "Write a Q2 portfolio review email",
  "Draft a rebalancing recommendation",
  "Write a market volatility outreach note",
  "Draft a retirement planning check-in",
];

export default function AdvisorPanel({ advisors, clients, advisorId, clientId, onAdvisor, onClient, onResult, onLoading, loading }) {
  const [prompt, setPrompt] = useState("");
  const meta = ADVISOR_META[advisorId] || {};

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    onLoading(true);
    onResult(null);
    try {
      const res = await runPrompt(advisorId, clientId, prompt);
      onResult(res);
    } catch (e) {
      onResult({ error: e.message });
    } finally {
      onLoading(false);
    }
  };

  return (
    <div style={S.wrap}>
      <div style={S.section}>
        <div style={S.label}>Advisor</div>
        <select style={S.select} value={advisorId} onChange={e => onAdvisor(e.target.value)}>
          {advisors.map(a => <option key={a.advisor_id} value={a.advisor_id}>{a.name}</option>)}
          {!advisors.length && <option value="ADV001">Surya T. Meesala</option>}
        </select>
        {meta.style && (
          <div style={{ display: "flex", flexDirection: "column", gap: 4, marginTop: 4 }}>
            <div style={S.infoRow}><span style={S.infoKey}>Style</span><span style={S.infoVal}>{meta.style}</span></div>
            <div style={S.infoRow}><span style={S.infoKey}>Tone</span><span style={S.infoVal}>{meta.tone}</span></div>
            <div style={{ marginTop: 4 }}>
              {(meta.spec || "").split(" · ").map(s => <span key={s} style={S.chip}>{s}</span>)}
            </div>
          </div>
        )}
      </div>

      <div style={S.divider} />

      <div style={S.section}>
        <div style={S.label}>Client</div>
        <select style={S.select} value={clientId} onChange={e => onClient(e.target.value)}>
          {clients.map(c => <option key={c.client_id} value={c.client_id}>{c.client_name}</option>)}
          {!clients.length && <option value="C001">Margaret Collins</option>}
        </select>
      </div>

      <div style={S.divider} />

      <div style={S.section}>
        <div style={S.label}>Quick Prompts</div>
        {PROMPTS.map(p => (
          <div key={p} onClick={() => setPrompt(p)}
            style={{ ...S.chip, cursor: "pointer", display: "block", marginBottom: 4, padding: "5px 8px" }}>
            {p}
          </div>
        ))}
      </div>

      <div style={S.section}>
        <div style={S.label}>Your Prompt</div>
        <textarea
          style={S.textarea}
          value={prompt}
          onChange={e => setPrompt(e.target.value)}
          placeholder="Write a Q2 portfolio review email for this client..."
        />
      </div>

      <button
        style={{ ...S.btn, ...(loading ? S.btnLoading : {}) }}
        onClick={handleGenerate}
        disabled={loading}
      >
        {loading ? "⚡ Generating..." : "⚡ Generate"}
      </button>
    </div>
  );
}
