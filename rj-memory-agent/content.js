// content.js — injected into the active page
if (!window.__rjAgentLoaded) {
  window.__rjAgentLoaded = true;
  window.__rjContainerCache = undefined; // reset on each fresh injection

  // Cache the working scroll container so we don't re-detect every call
  let _cachedContainer = window.__rjContainerCache;

  function getScrollContainer() {
    if (_cachedContainer !== undefined) return _cachedContainer;

    // Walk every element and find which ones actually move when scrolled
    const streamlitSelectors = [
      '[data-testid="stAppViewBlockContainer"]',
      '[data-testid="stAppViewContainer"]',
      '[data-testid="stMain"]',
      '.main > div',
      '.main',
      '.block-container',
      'section.main',
    ];

    // Try Streamlit-specific selectors first by testing if they actually scroll
    for (const sel of streamlitSelectors) {
      const el = document.querySelector(sel);
      if (!el) continue;
      const before = el.scrollTop;
      el.scrollTop = before + 1;
      const moved = el.scrollTop !== before;
      el.scrollTop = before;
      if (moved) { _cachedContainer = el; return el; }
    }

    // Try window scroll
    const winBefore = window.scrollY;
    window.scrollBy(0, 1);
    if (window.scrollY !== winBefore) {
      window.scrollBy(0, -1);
      _cachedContainer = null; // null means use window
      return null;
    }
    window.scrollBy(0, -1);

    // Last resort: find the deepest element with the most scrollable height
    let best = null, bestScore = 0;
    document.querySelectorAll('*').forEach(el => {
      const score = el.scrollHeight - el.clientHeight;
      if (score > 100 && score > bestScore) {
        const style = getComputedStyle(el);
        if (style.overflowY === 'auto' || style.overflowY === 'scroll') {
          best = el; bestScore = score;
        }
      }
    });
    _cachedContainer = best;
    return best;
  }

  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {

    if (message.action === "ping") {
      sendResponse({ alive: true });
      return true;
    }

    if (message.action === "getPageHeight") {
      const c = getScrollContainer();
      sendResponse({
        totalHeight:  c ? c.scrollHeight : document.documentElement.scrollHeight,
        windowHeight: c ? c.clientHeight  : window.innerHeight,
        scrollTop:    c ? c.scrollTop     : window.scrollY,
        usesContainer: !!c,
      });
      return true;
    }

    if (message.action === "scrollTo") {
      const c = getScrollContainer();
      if (c) c.scrollTo({ top: message.position, behavior: "instant" });
      else   window.scrollTo({ top: message.position, behavior: "instant" });
      setTimeout(() => sendResponse({ done: true }), message.wait || 500);
      return true;
    }

    if (message.action === "scrollDown") {
      const amount = message.amount || window.innerHeight * 0.85;

      // Try every candidate — whichever one's scrollTop actually changes wins
      const candidates = [
        document.querySelector('[data-testid="stAppViewBlockContainer"]'),
        document.querySelector('[data-testid="stAppViewContainer"]'),
        document.querySelector('[data-testid="stMain"]'),
        document.querySelector('.main'),
        document.querySelector('.block-container'),
        document.documentElement,
        document.body,
      ].filter(Boolean);

      let scrolled = false;
      for (const el of candidates) {
        const before = el.scrollTop;
        el.scrollTop += amount;
        if (el.scrollTop !== before) { scrolled = true; break; }
      }

      // Also try window scroll as a fallback
      if (!scrolled) {
        const before = window.scrollY;
        window.scrollBy(0, amount);
        scrolled = window.scrollY !== before;
      }

      setTimeout(() => {
        // Report position from whichever source has scroll
        const winY = window.scrollY;
        const docH = document.documentElement.scrollHeight;
        sendResponse({
          done: true,
          atBottom: winY + window.innerHeight >= docH - 30,
          scrollTop: winY,
          scrolled,
        });
      }, message.wait || 500);
      return true;
    }

    if (message.action === "scrollToTop") {
      _cachedContainer = undefined; // reset so next call re-detects
      const c = getScrollContainer();
      if (c) c.scrollTo({ top: 0, behavior: "instant" });
      else   window.scrollTo({ top: 0, behavior: "instant" });
      setTimeout(() => sendResponse({ done: true }), 200);
      return true;
    }

    if (message.action === "clickElement") {
      const { text, selector } = message;
      let el = null;

      if (selector) {
        el = document.querySelector(selector);
      }

      if (!el && text) {
        // Find by exact text match first, then partial
        const allEls = document.querySelectorAll('button, a, [role="tab"], [role="button"], li, span, div');
        for (const candidate of allEls) {
          const t = candidate.textContent.trim();
          if (t === text || t.startsWith(text)) { el = candidate; break; }
        }
        if (!el) {
          for (const candidate of allEls) {
            if (candidate.textContent.toLowerCase().includes(text.toLowerCase())) { el = candidate; break; }
          }
        }
      }

      if (el) {
        el.click();
        setTimeout(() => sendResponse({ success: true, clicked: el.textContent.trim().slice(0, 60) }), 600);
      } else {
        sendResponse({ success: false, error: `Element not found: "${text}"` });
      }
      return true;
    }

    if (message.action === "showAgentOverlay") {
      if (document.getElementById("__rj_overlay__")) {
        // Already showing — just update the label
        const lbl = document.getElementById("__rj_banner_text__");
        if (lbl && message.label) lbl.textContent = message.label;
        sendResponse({ done: true });
        return true;
      }

      const overlay = document.createElement("div");
      overlay.id = "__rj_overlay__";
      overlay.innerHTML = `
        <style>
          #__rj_overlay__ * { box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
          /* Banner — centered floating pill */
          #__rj_banner__ {
            position: fixed;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            z-index: 2147483647;
            background: rgba(0, 28, 79, 0.92);
            color: white;
            display: flex; flex-direction: column; align-items: center; gap: 10px;
            padding: 22px 32px;
            border-radius: 16px;
            border: 1.5px solid #22c55e;
            font-size: 14px; font-weight: 600;
            box-shadow: 0 0 32px rgba(34,197,94,0.35), 0 8px 32px rgba(0,0,0,0.5);
            backdrop-filter: blur(6px);
            animation: __rj_blink_border__ 1.2s ease-in-out infinite;
            min-width: 260px; text-align: center;
          }
          @keyframes __rj_blink_border__ {
            0%,100% { border-color: #22c55e; box-shadow: 0 0 32px rgba(34,197,94,0.35), 0 8px 32px rgba(0,0,0,0.5); }
            50%      { border-color: #86efac; box-shadow: 0 0 48px rgba(34,197,94,0.7),  0 8px 32px rgba(0,0,0,0.5); }
          }
          #__rj_banner__ .rj-logo {
            color: #C8A034; font-weight: 800; letter-spacing: 1.5px; font-size: 11px;
          }
          #__rj_banner__ .rj-dot-row {
            display: flex; gap: 6px; align-items: center;
          }
          #__rj_banner__ .rj-dot {
            width: 9px; height: 9px; border-radius: 50%; background: #22c55e;
            animation: __rj_blink_dot__ 1.2s ease-in-out infinite;
          }
          #__rj_banner__ .rj-dot:nth-child(2) { animation-delay: 0.2s; }
          #__rj_banner__ .rj-dot:nth-child(3) { animation-delay: 0.4s; }
          @keyframes __rj_blink_dot__ {
            0%,100% { opacity: 1;   transform: scale(1); }
            50%      { opacity: 0.2; transform: scale(0.6); }
          }
          #__rj_banner_text__ {
            font-size: 13px; color: #e2e8f0; font-weight: 500; line-height: 1.4;
            animation: __rj_blink_text__ 2.4s ease-in-out infinite;
          }
          @keyframes __rj_blink_text__ {
            0%,100% { opacity: 1; }
            50%      { opacity: 0.6; }
          }
          /* Corner brackets */
          .rj-corner {
            position: fixed; z-index: 2147483646; width: 28px; height: 28px;
            pointer-events: none;
          }
          .rj-corner svg { width: 100%; height: 100%; }
          .rj-corner-tl { top: 8px;  left: 8px;  }
          .rj-corner-tr { top: 8px;  right: 8px; transform: scaleX(-1); }
          .rj-corner-bl { bottom: 8px; left: 8px;  transform: scaleY(-1); }
          .rj-corner-br { bottom: 8px; right: 8px; transform: scale(-1,-1); }
          .rj-corner path {
            stroke: #22c55e; stroke-width: 3; fill: none; stroke-linecap: round;
          }
          .rj-corner {
            animation: __rj_corner_blink__ 0.8s ease-in-out infinite;
          }
          @keyframes __rj_corner_blink__ {
            0%,100% { opacity: 1; filter: drop-shadow(0 0 6px #22c55e); }
            50%      { opacity: 0; filter: drop-shadow(0 0 0px #22c55e); }
          }
          .rj-corner-tr { animation-delay: 0.2s; }
          .rj-corner-bl { animation-delay: 0.4s; }
          .rj-corner-br { animation-delay: 0.6s; }
          /* Scan line */
          #__rj_scanline__ {
            position: fixed; left: 0; right: 0; height: 2px; z-index: 2147483645;
            background: linear-gradient(90deg, transparent, #22c55e 40%, #86efac 60%, transparent);
            pointer-events: none; top: 0;
            animation: __rj_scan__ 2s linear infinite;
            box-shadow: 0 0 8px #22c55e;
          }
          @keyframes __rj_scan__ {
            0%   { top: 0; opacity: 1; }
            90%  { top: calc(100vh - 4px); opacity: 1; }
            100% { top: calc(100vh - 4px); opacity: 0; }
          }
        </style>
        <div id="__rj_banner__">
          <span class="rj-logo">RAYMOND JAMES</span>
          <div class="rj-dot-row">
            <span class="rj-dot"></span>
            <span class="rj-dot"></span>
            <span class="rj-dot"></span>
          </div>
          <span id="__rj_banner_text__">${message.label || "AI Agent is analyzing this page…"}</span>
        </div>
        <div class="rj-corner rj-corner-tl"><svg viewBox="0 0 28 28"><path d="M 28 4 L 4 4 L 4 28"/></svg></div>
        <div class="rj-corner rj-corner-tr"><svg viewBox="0 0 28 28"><path d="M 28 4 L 4 4 L 4 28"/></svg></div>
        <div class="rj-corner rj-corner-bl"><svg viewBox="0 0 28 28"><path d="M 28 4 L 4 4 L 4 28"/></svg></div>
        <div class="rj-corner rj-corner-br"><svg viewBox="0 0 28 28"><path d="M 28 4 L 4 4 L 4 28"/></svg></div>
        <div id="__rj_scanline__"></div>
      `;
      document.body.appendChild(overlay);
      sendResponse({ done: true });
      return true;
    }

    if (message.action === "hideAgentOverlay") {
      const el = document.getElementById("__rj_overlay__");
      if (el) el.remove();
      sendResponse({ done: true });
      return true;
    }

    if (message.action === "updateAgentOverlay") {
      const lbl = document.getElementById("__rj_banner_text__");
      if (lbl) lbl.textContent = message.label || "";
      sendResponse({ done: true });
      return true;
    }

    if (message.action === "freezeAnimations") {
      if (!document.getElementById("__rj_freeze__")) {
        const s = document.createElement("style");
        s.id = "__rj_freeze__";
        s.textContent = "*:not(#__rj_overlay__):not(#__rj_overlay__ *):not(#__rj_banner__):not(#__rj_scanline__):not(.rj-corner):not(.rj-corner *):not(.rj-dot) { animation: none !important; transition: none !important; }";
        document.head.appendChild(s);
      }
      sendResponse({ done: true });
      return true;
    }

    if (message.action === "unfreezeAnimations") {
      const el = document.getElementById("__rj_freeze__");
      if (el) el.remove();
      sendResponse({ done: true });
      return true;
    }
  });
}
