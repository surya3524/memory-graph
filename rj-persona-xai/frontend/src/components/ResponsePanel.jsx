import { useState } from "react";

const S = {
  wrap: { padding: 16, display: "flex", flexDirection: "column", gap: 10 },
  title: { fontSize: 13, fontWeight: 600, color: "var(--gold)" },
  box: {
    background: "var(--card)", border: "1px solid var(--border)", borderRadius: 6,
    padding: 14, fontSize: 13, color: "var(--text)", lineHeight: 1.7,
    minHeight: 120, whiteSpace: "pre-wrap"
  },
  footer: { display: "flex", gap: 10, alignItems: "center" },
  btn: {
    background: "var(--cardHi)", border: "1px solid var(--border)",
    color: "var(--text)", borderRadius: 6, padding: "6px 14px",
    fontSize: 12, cursor: "pointer"
  },
  btnDisabled: {
    background: "var(--cardHi)", border: "1px solid var(--border)",
    color: "var(--muted)", borderRadius: 6, padding: "6px 14px",
    fontSize: 12, cursor: "not-allowed", opacity: 0.5
  },
  tokens: { fontSize: 11, color: "var(--muted)", marginLeft: "auto" },
  skeleton: {
    background: "linear-gradient(90deg, var(--card) 25%, var(--cardHi) 50%, var(--card) 75%)",
    backgroundSize: "200% 100%", animation: "shimmer 1.4s infinite",
    borderRadius: 6, height: 14, marginBottom: 8
  },
  empty: { color: "var(--muted)", fontSize: 12 },
  copied: { color: "var(--green)", fontSize: 11 },
};

export default function ResponsePanel({ result, loading }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    if (!result?.llm_response) return;
    navigator.clipboard.writeText(result.llm_response);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div style={S.wrap}>
      <div style={S.title}>AI Response — Advisor Voice</div>
      <div style={S.box}>
        {loading && (
          <div>
            <div style={{ ...S.skeleton, width: "90%" }} />
            <div style={{ ...S.skeleton, width: "75%" }} />
            <div style={{ ...S.skeleton, width: "85%" }} />
            <div style={{ ...S.skeleton, width: "60%" }} />
          </div>
        )}
        {!loading && result?.llm_response && result.llm_response}
        {!loading && result?.error && (
          <span style={{ color: "var(--red)" }}>Error: {result.error}</span>
        )}
        {!loading && !result && (
          <span style={S.empty}>Response will appear here after you generate…</span>
        )}
      </div>
      <div style={S.footer}>
        <button
          style={result?.llm_response ? S.btn : S.btnDisabled}
          onClick={handleCopy}
          disabled={!result?.llm_response}
        >
          {copied ? "✓ Copied" : "Copy"}
        </button>
        <button style={S.btnDisabled} disabled title="Review required before sending">
          Send to Client (advisor review required)
        </button>
        {result?.tokens_used && (
          <span style={S.tokens}>{result.tokens_used} tokens</span>
        )}
        {copied && <span style={S.copied}>Copied to clipboard</span>}
      </div>
      <style>{`@keyframes shimmer { 0%{background-position:200% 0} 100%{background-position:-200% 0} }`}</style>
    </div>
  );
}
