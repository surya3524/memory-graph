// content.js — injected into the active page
if (!window.__rjAgentLoaded) {
  window.__rjAgentLoaded = true;

  function getScrollContainer() {
    const selectors = [
      '[data-testid="stAppViewContainer"]',
      '.main',
      '[data-testid="stMain"]',
      '.block-container',
    ];
    for (const sel of selectors) {
      const el = document.querySelector(sel);
      if (el && el.scrollHeight > el.clientHeight + 50) return el;
    }
    const candidates = [document.documentElement, document.body];
    let best = document.documentElement;
    for (const el of candidates) {
      if (el.scrollHeight > best.scrollHeight) best = el;
    }
    return best.scrollHeight > window.innerHeight + 50 ? best : null;
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
