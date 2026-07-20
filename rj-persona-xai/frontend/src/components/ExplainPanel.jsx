const NODE_COLORS = {
  goal: "#FFB81C", risk_profile: "#003087", portfolio: "#00C46A",
  behavior: "#3B9EFF", life_event: "#FF9500", transaction: "#7A9BB5"
};

const S = {
  wrap: { width: 340, padding: 16, display: "flex", flexDirection: "column", gap: 10, borderLeft: "1px solid var(--border)" },
  title: { fontSize: 13, fontWeight: 600, color: "var(--gold)" },
  subtitle: { fontSize: 11, color: "var(--muted)", textTransform: "uppercase", letterSpacing: 1, marginBottom: 4 },
  barWrap: { display: "flex", flexDirection: "column", gap: 6 },
  barRow: { display: "flex", flexDirection: "column", gap: 2 },
  barLabel: { display: "flex", justifyContent: "space-between", fontSize: 11 },
  barTrack: { height: 10, background: "var(--card)", borderRadius: 5, overflow: "hidden" },
  barFill: { height: "100%", borderRadius: 5, transition: "width 0.6s ease" },
  counterfactual: {
    background: "rgba(59,158,255,0.08)", border: "1px solid rgba(59,158,255,0.25)",
    borderRadius: 6, padding: "10px 12px", fontSize: 12, color: "var(--text)", lineHeight: 1.6
  },
  cfLabel: { color: "var(--blue)", fontWeight: 600, marginBottom: 4, fontSize: 11 },
  footer: { display: "flex", justifyContent: "space-between", alignItems: "center" },
  confidence: { fontSize: 12, color: "var(--green)", fontWeight: 600 },
  finra: {
    background: "rgba(0,196,106,0.1)", border: "1px solid rgba(0,196,106,0.3)",
    borderRadius: 4, padding: "4px 10px", fontSize: 11, color: "var(--green)", cursor: "pointer"
  },
  empty: { fontSize: 12, color: "var(--muted)" },
};

export default function ExplainPanel({ result }) {
  const xai = result?.xai_result;

  return (
    <div style={S.wrap}>
      <div style={S.title}>Explainability (XAI)</div>

      <div>
        <div style={S.subtitle}>What drove this recommendation</div>
        <div style={S.barWrap}>
          {xai?.node_attributions?.slice(0, 5).map(a => (
            <div key={a.node_id} style={S.barRow}>
              <div style={S.barLabel}>
                <span style={{ color: NODE_COLORS[a.node_type] || "var(--text)" }}>
                  {a.label.length > 30 ? a.label.slice(0, 30) + "…" : a.label}
                </span>
                <span style={{ color: "var(--muted)" }}>{a.contribution_pct}%</span>
              </div>
              <div style={S.barTrack}>
                <div style={{
                  ...S.barFill,
                  width: `${a.contribution_pct}%`,
                  background: NODE_COLORS[a.node_type] || "var(--blue)"
                }} />
              </div>
            </div>
          ))}
          {!xai && (
            <div style={S.empty}>Attribution chart appears after generation.</div>
          )}
        </div>
      </div>

      <div>
        <div style={S.cfLabel}>💡 Counterfactual</div>
        <div style={S.counterfactual}>
          {xai?.counterfactual || "Counterfactual will appear after generation."}
        </div>
      </div>

      <div style={S.footer}>
        <div style={S.confidence}>
          {xai ? `Confidence: ${Math.round(xai.confidence * 100)}%` : "Confidence: —"}
        </div>
        <div style={S.finra} title="Full audit log stored: composed prompt, attribution scores, counterfactual">
          FINRA Log Ready ✓
        </div>
      </div>
    </div>
  );
}
