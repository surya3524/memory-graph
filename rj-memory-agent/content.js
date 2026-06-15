// content.js
// Injected into the active webpage — handles scrolling on behalf of background.js

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {

  if (message.action === "getPageHeight") {
    sendResponse({
      totalHeight: document.body.scrollHeight,
      windowHeight: window.innerHeight,
    });
    return true;
  }

  if (message.action === "scrollTo") {
    window.scrollTo({ top: message.position, behavior: "instant" });
    // Wait for any lazy-loaded content to settle before confirming
    setTimeout(() => sendResponse({ done: true }), message.wait || 300);
    return true;
  }

  if (message.action === "scrollToTop") {
    window.scrollTo({ top: 0, behavior: "instant" });
    setTimeout(() => sendResponse({ done: true }), 200);
    return true;
  }

  if (message.action === "freezeAnimations") {
    const style = document.createElement("style");
    style.id = "__rj_freeze__";
    style.textContent = "*, *::before, *::after { animation: none !important; transition: none !important; }";
    document.head.appendChild(style);
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
