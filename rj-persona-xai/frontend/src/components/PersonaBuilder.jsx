import { useState } from "react";

const S = {
  wrap: { width: 280, padding: 16, borderLeft: "1px solid var(--border)", display: "flex", flexDirection: "column", gap: 10 },
  title: { fontSize: 13, fontWeight: 600, color: "var(--gold)" },
  toggle: {
    fontSize: 11, color: "var(--blue)", cursor: "pointer",
    textDecoration: "underline", textUnderlineOffset: 2
  },
  box: {
    background: "var(--card)", border: "1px solid var(--border)",
    borderRadius: 6, padding: 10, fontSize: 11, color: "var(--muted)",
    fontFamily: "monospace", lineHeight: 1.6, maxHeight: 180, overflowY: "auto"
  },
  tag: {
    display: "inline-block", borderRadius: 3, padding: "1px 5px",
    fontSize: 10, fontWeight: 600, marginRight: 2
  },
  row: { display: "flex", justifyContent: "space-between", alignItems: "center" },
  count: { fontSize: 11, color: "var(--green)" },
  section: { marginBottom: 6 },
  sectionLabel: { fontSize: 10, textTransform: "uppercase", letterSpacing: 1, color: "var(--muted)", marginBottom: 4 },
};

const SECTION_COLORS = {
  profile:  { bg: "rgba(255,184,28,0.15)", color: "#FFB81C" },
  samples:  { bg: "rgba(59,158,255,0.15)", color: "#3B9EFF" },
  context:  { bg: "rgba(0,196,106,0.15)",  color: "#00C46A" },
};

export default function PersonaBuilder({ advisorId, result }) {
  const [open, setOpen] = useState(false);
  const persona = result?.persona_injected;
  const graphCtx = result?.graph_context_used || [];

  const fields = persona ? persona.fields_injected || 6 : 6;
  const samples = persona ? persona.samples_count || 2 : 2;
  const nodes = graphCtx.length || 4;

  return (
    <div style={S.wrap}>
      <div style={S.row}>
        <div style={S.title}>Persona Injection</div>
        <span style={S.toggle} onClick={() => setOpen(o => !o)}>
          {open ? "collapse" : "expand"}
        </span>
      </div>

      <div style={S.count}>
        Injecting {fields} profile fields · {samples} writing samples · {nodes} graph nodes
      </div>

      {open && (
        <div style={S.box}>
          <div style={S.section}>
            <div style={S.sectionLabel}>Advisor Profile</div>
            {["Name · CRD · Branch", "Specialty", "Communication style", "Tone", "Client base", "Compliance scope"]
              .map(f => (
                <div key={f}>
                  <span style={{ ...S.tag, ...SECTION_COLORS.profile }}>{f}</span>
                </div>
              ))}
          </div>
          <div style={S.section}>
            <div style={S.sectionLabel}>Writing Samples ({samples})</div>
            <span style={{ ...S.tag, ...SECTION_COLORS.samples }}>Past email 1</span>
            <span style={{ ...S.tag, ...SECTION_COLORS.samples }}>Past email 2</span>
          </div>
          <div style={S.section}>
            <div style={S.sectionLabel}>Graph Context ({nodes} nodes)</div>
            {graphCtx.length > 0
              ? graphCtx.map(s => (
                  <div key={s}><span style={{ ...S.tag, ...SECTION_COLORS.context }}>{s}</span></div>
                ))
              : ["Goal", "Portfolio", "Behavior", "Life event"].map(s => (
                  <div key={s}><span style={{ ...S.tag, ...SECTION_COLORS.context }}>{s}</span></div>
                ))}
          </div>
        </div>
      )}

      {result?.composed_prompt && open && (
        <>
          <div style={{ fontSize: 11, color: "var(--muted)", marginTop: 4 }}>Composed system prompt:</div>
          <div style={{ ...S.box, maxHeight: 140, fontSize: 10 }}>
            {result.composed_prompt.slice(0, 600)}…
          </div>
        </>
      )}

      {!result && (
        <div style={{ fontSize: 11, color: "var(--muted)", marginTop: 4 }}>
          Generate a response to see the composed prompt live.
        </div>
      )}
    </div>
  );
}
