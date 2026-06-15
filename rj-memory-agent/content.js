// content.js — injected into the active page
// Guard prevents duplicate listeners when injected multiple times
if (!window.__rjAgentLoaded) {
  window.__rjAgentLoaded = true;

  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {

    if (message.action === "ping") {
      sendResponse({ alive: true });
      return true;
    }

    if (message.action === "getPageHeight") {
      sendResponse({
        totalHeight: Math.max(document.body.scrollHeight, document.documentElement.scrollHeight),
        windowHeight: window.innerHeight,
      });
      return true;
    }

    if (message.action === "scrollTo") {
      window.scrollTo({ top: message.position, behavior: "instant" });
      setTimeout(() => sendResponse({ done: true, actual: window.scrollY }), message.wait || 400);
      return true;
    }

    if (message.action === "scrollToTop") {
      window.scrollTo({ top: 0, behavior: "instant" });
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
