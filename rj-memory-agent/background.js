// background.js — service worker
const MAX_SCREENSHOTS = 5;

// Open side panel when extension icon is clicked
chrome.action.onClicked.addListener(tab => {
  chrome.sidePanel.open({ tabId: tab.id });
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "captureFullPage") {
    captureFullPage()
      .then(result => sendResponse({ success: true, ...result }))
      .catch(err  => sendResponse({ success: false, error: err.message }));
    return true;
  }
});

async function captureFullPage() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab) throw new Error("No active tab found.");
  if (tab.url.startsWith("chrome://") || tab.url.startsWith("chrome-extension://")) {
    throw new Error("Cannot scan Chrome internal pages. Please navigate to a real webpage first.");
  }

  // Always inject fresh — the guard in content.js prevents duplicate listeners
  await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    files: ["content.js"],
  });
  await sleep(200);

  // Confirm content script is alive before proceeding
  const ping = await safeSend(tab.id, { action: "ping" });
  if (!ping?.alive) throw new Error("Could not connect to page. Try refreshing the page.");

  await chrome.tabs.sendMessage(tab.id, { action: "freezeAnimations" });

  const pageInfo = await chrome.tabs.sendMessage(tab.id, { action: "getPageHeight" });
  const { totalHeight, windowHeight } = pageInfo;

  const totalSteps = Math.ceil(totalHeight / windowHeight);
  const steps      = Math.min(totalSteps, MAX_SCREENSHOTS);

  const screenshots = [];

  for (let i = 0; i < steps; i++) {
    // Distribute evenly: step 0 = top, last step = bottom
    const position = steps === 1
      ? 0
      : Math.round((i / (steps - 1)) * Math.max(0, totalHeight - windowHeight));

    // Scroll and wait for page to settle
    await chrome.tabs.sendMessage(tab.id, { action: "scrollTo", position, wait: 500 });
    await sleep(600); // Extra buffer for dynamic content / lazy loading

    const dataUrl = await chrome.tabs.captureVisibleTab(tab.windowId, {
      format: "jpeg",
      quality: 85,
    });
    screenshots.push(dataUrl);
  }

  // Restore
  await chrome.tabs.sendMessage(tab.id, { action: "scrollToTop" });
  await sleep(200);
  await chrome.tabs.sendMessage(tab.id, { action: "unfreezeAnimations" });

  return {
    screenshots,
    meta: {
      totalHeight,
      windowHeight,
      stepsUsed: steps,
      totalStepsPossible: totalSteps,
      capped: totalSteps > MAX_SCREENSHOTS,
    },
  };
}

// Safe message sender — returns null instead of throwing if tab isn't ready
function safeSend(tabId, message) {
  return new Promise(resolve => {
    chrome.tabs.sendMessage(tabId, message, response => {
      if (chrome.runtime.lastError) resolve(null);
      else resolve(response);
    });
  });
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
