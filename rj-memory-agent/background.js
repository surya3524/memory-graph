// background.js — service worker
// Opens the side panel on extension icon click, coordinates scroll + screenshot

const MAX_SCREENSHOTS = 5;

// Open side panel when the extension icon is clicked
chrome.action.onClicked.addListener(tab => {
  chrome.sidePanel.open({ tabId: tab.id });
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "captureFullPage") {
    captureFullPage()
      .then(result => sendResponse({ success: true, ...result }))
      .catch(err => sendResponse({ success: false, error: err.message }));
    return true;
  }
});

async function captureFullPage() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab) throw new Error("No active tab found.");

  // Programmatically inject content.js — fixes "receiving end does not exist"
  // for tabs that were already open before the extension was loaded
  await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    files: ["content.js"],
  });

  // Small pause to let content script initialize
  await sleep(150);

  // Freeze animations for clean screenshots
  await chrome.tabs.sendMessage(tab.id, { action: "freezeAnimations" });

  const pageInfo = await chrome.tabs.sendMessage(tab.id, { action: "getPageHeight" });
  const { totalHeight, windowHeight } = pageInfo;

  const totalSteps = Math.ceil(totalHeight / windowHeight);
  const steps = Math.min(totalSteps, MAX_SCREENSHOTS);

  const screenshots = [];

  for (let i = 0; i < steps; i++) {
    const position = steps === 1
      ? 0
      : Math.round((i / (steps - 1)) * Math.max(0, totalHeight - windowHeight));

    await chrome.tabs.sendMessage(tab.id, { action: "scrollTo", position, wait: 400 });
    await sleep(450);

    const dataUrl = await chrome.tabs.captureVisibleTab(tab.windowId, {
      format: "jpeg",
      quality: 82,
    });
    screenshots.push(dataUrl);
  }

  await chrome.tabs.sendMessage(tab.id, { action: "scrollToTop" });
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

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
