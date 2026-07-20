import { useEffect, useRef, useState } from "react";
import { getGraph } from "../api/client";

const NODE_COLORS = {
  goal: "#FFB81C", risk_profile: "#003087", portfolio: "#00C46A",
  behavior: "#3B9EFF", life_event: "#FF9500", transaction: "#7A9BB5"
};

const S = {
  wrap: { padding: 16, height: "100%", display: "flex", flexDirection: "column" },
  title: { fontSize: 13, fontWeight: 600, color: "var(--gold)", marginBottom: 8 },
  canvas: { flex: 1, position: "relative", minHeight: 220 },
  legend: { display: "flex", flexWrap: "wrap", gap: 8, marginTop: 8 },
  dot: { width: 10, height: 10, borderRadius: "50%", display: "inline-block", marginRight: 4 },
  legItem: { display: "flex", alignItems: "center", fontSize: 11, color: "var(--muted)" },
  tooltip: {
    position: "absolute", background: "var(--cardHi)", border: "1px solid var(--border)",
    borderRadius: 6, padding: "8px 12px", fontSize: 12, color: "var(--text)",
    pointerEvents: "none", zIndex: 10, maxWidth: 200
  }
};

function useDimensions(ref) {
  const [dims, setDims] = useState({ w: 400, h: 220 });
  useEffect(() => {
    if (!ref.current) return;
    const obs = new ResizeObserver(([e]) => {
      setDims({ w: e.contentRect.width, h: e.contentRect.height });
    });
    obs.observe(ref.current);
    return () => obs.disconnect();
  }, []);
  return dims;
}

function forceLayout(nodes, edges, w, h, iterations = 80) {
  const pos = {};
  nodes.forEach((n, i) => {
    const angle = (i / nodes.length) * Math.PI * 2;
    pos[n.id] = { x: w / 2 + Math.cos(angle) * w * 0.32, y: h / 2 + Math.sin(angle) * h * 0.32 };
  });
  const k = Math.sqrt((w * h) / nodes.length) * 0.9;
  for (let iter = 0; iter < iterations; iter++) {
    const disp = {};
    nodes.forEach(n => { disp[n.id] = { x: 0, y: 0 }; });
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const u = nodes[i].id, v = nodes[j].id;
        const dx = pos[u].x - pos[v].x, dy = pos[u].y - pos[v].y;
        const dist = Math.max(Math.sqrt(dx * dx + dy * dy), 0.01);
        const rep = (k * k) / dist;
        disp[u].x += (dx / dist) * rep; disp[u].y += (dy / dist) * rep;
        disp[v].x -= (dx / dist) * rep; disp[v].y -= (dy / dist) * rep;
      }
    }
    edges.forEach(e => {
      const u = e.source, v = e.target;
      if (!pos[u] || !pos[v]) return;
      const dx = pos[u].x - pos[v].x, dy = pos[u].y - pos[v].y;
      const dist = Math.max(Math.sqrt(dx * dx + dy * dy), 0.01);
      const att = (dist * dist) / k;
      disp[u].x -= (dx / dist) * att * e.strength;
      disp[u].y -= (dy / dist) * att * e.strength;
      disp[v].x += (dx / dist) * att * e.strength;
      disp[v].y += (dy / dist) * att * e.strength;
    });
    const temp = k * (1 - iter / iterations);
    nodes.forEach(n => {
      const d = disp[n.id];
      const len = Math.max(Math.sqrt(d.x * d.x + d.y * d.y), 0.01);
      pos[n.id].x = Math.max(40, Math.min(w - 40, pos[n.id].x + (d.x / len) * Math.min(len, temp)));
      pos[n.id].y = Math.max(40, Math.min(h - 40, pos[n.id].y + (d.y / len) * Math.min(len, temp)));
    });
  }
  return pos;
}

export default function ClientGraphPanel({ clientId }) {
  const [graphData, setGraphData] = useState(null);
  const [tooltip, setTooltip] = useState(null);
  const containerRef = useRef(null);
  const { w, h } = useDimensions(containerRef);

  useEffect(() => {
    setGraphData(null);
    getGraph(clientId).then(setGraphData).catch(() => {});
  }, [clientId]);

  const pos = graphData ? forceLayout(graphData.nodes, graphData.edges, w, h) : {};

  return (
    <div style={S.wrap}>
      <div style={S.title}>Client Memory Graph</div>
      <div ref={containerRef} style={S.canvas}>
        {graphData && (
          <svg width={w} height={h} style={{ position: "absolute", top: 0, left: 0 }}>
            <defs>
              <marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
                <path d="M0,0 L0,6 L8,3 z" fill="#1A304E" />
              </marker>
            </defs>
            {graphData.edges.map((e, i) => {
              const s = pos[e.source], t = pos[e.target];
              if (!s || !t) return null;
              return (
                <line key={i} x1={s.x} y1={s.y} x2={t.x} y2={t.y}
                  stroke="#1A304E" strokeWidth={e.strength * 3}
                  strokeOpacity={0.7} markerEnd="url(#arrow)" />
              );
            })}
            {graphData.nodes.map(n => {
              const p = pos[n.id];
              if (!p) return null;
              const r = 18 + n.weight * 14;
              const color = NODE_COLORS[n.type] || "#4A7090";
              return (
                <g key={n.id} style={{ cursor: "pointer" }}
                  onMouseEnter={() => setTooltip({ x: p.x, y: p.y, label: n.label, type: n.type })}
                  onMouseLeave={() => setTooltip(null)}>
                  <circle cx={p.x} cy={p.y} r={r} fill={color} fillOpacity={0.18} stroke={color} strokeWidth={2} />
                  <text x={p.x} y={p.y + 4} textAnchor="middle" fontSize={10}
                    fill={color} fontWeight={600} style={{ userSelect: "none" }}>
                    {n.type.replace("_", " ")}
                  </text>
                </g>
              );
            })}
          </svg>
        )}
        {tooltip && (
          <div style={{ ...S.tooltip, left: tooltip.x + 16, top: tooltip.y - 16 }}>
            <div style={{ color: NODE_COLORS[tooltip.type], fontWeight: 600, marginBottom: 2 }}>
              {tooltip.type.replace("_", " ")}
            </div>
            {tooltip.label}
          </div>
        )}
        {!graphData && (
          <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center",
            justifyContent: "center", color: "var(--muted)" }}>
            Loading graph…
          </div>
        )}
      </div>
      <div style={S.legend}>
        {Object.entries(NODE_COLORS).map(([type, color]) => (
          <div key={type} style={S.legItem}>
            <span style={{ ...S.dot, background: color }} />
            {type.replace("_", " ")}
          </div>
        ))}
      </div>
    </div>
  );
}
