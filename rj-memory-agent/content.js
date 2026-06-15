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
      const c = getScrollContainer();
      const amount = message.amount || (c ? c.clientHeight : window.innerHeight) * 0.85;
      const current = c ? c.scrollTop : window.scrollY;
      if (c) c.scrollTo({ top: current + amount, behavior: "instant" });
      else   window.scrollTo({ top: current + amount, behavior: "instant" });
      setTimeout(() => {
        const newPos = c ? c.scrollTop : window.scrollY;
        const totalH = c ? c.scrollHeight : document.documentElement.scrollHeight;
        const winH   = c ? c.clientHeight  : window.innerHeight;
        sendResponse({ done: true, atBottom: newPos + winH >= totalH - 20, scrollTop: newPos });
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

    if (message.action === "freezeAnimations") {
      if (!document.getElementById("__rj_freeze__")) {
        const s = document.createElement("style");
        s.id = "__rj_freeze__";
        s.textContent = "*, *::before, *::after { animation: none !important; transition: none !important; }";
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
