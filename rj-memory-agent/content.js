// content.js — injected into the active page
if (!window.__rjAgentLoaded) {
  window.__rjAgentLoaded = true;

  // Find the real scrollable container — handles Streamlit, standard pages, etc.
  function getScrollContainer() {
    // Streamlit-specific containers
    const streamlitSelectors = [
      '[data-testid="stAppViewContainer"]',
      '.main',
      '[data-testid="stMain"]',
      '.block-container',
    ];
    for (const sel of streamlitSelectors) {
      const el = document.querySelector(sel);
      if (el && el.scrollHeight > el.clientHeight + 50) return el;
    }
    // Generic: find the element with the most scrollable height
    const candidates = [document.documentElement, document.body];
    let best = document.documentElement;
    for (const el of candidates) {
      if (el.scrollHeight > best.scrollHeight) best = el;
    }
    // If nothing is truly taller than the viewport, fallback to window scroll
    return best.scrollHeight > window.innerHeight + 50 ? best : null;
  }

  function scrollContainer() {
    return getScrollContainer();
  }

  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {

    if (message.action === "ping") {
      sendResponse({ alive: true });
      return true;
    }

    if (message.action === "getPageHeight") {
      const container = scrollContainer();
      const totalHeight  = container ? container.scrollHeight : Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
      const windowHeight = container ? container.clientHeight  : window.innerHeight;
      sendResponse({ totalHeight, windowHeight, usesContainer: !!container });
      return true;
    }

    if (message.action === "scrollTo") {
      const container = scrollContainer();
      if (container) {
        container.scrollTo({ top: message.position, behavior: "instant" });
      } else {
        window.scrollTo({ top: message.position, behavior: "instant" });
      }
      setTimeout(() => sendResponse({ done: true, actual: container ? container.scrollTop : window.scrollY }), message.wait || 500);
      return true;
    }

    if (message.action === "scrollToTop") {
      const container = scrollContainer();
      if (container) container.scrollTo({ top: 0, behavior: "instant" });
      else window.scrollTo({ top: 0, behavior: "instant" });
      setTimeout(() => sendResponse({ done: true }), 200);
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
