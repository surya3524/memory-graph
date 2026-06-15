// background.js
// Service worker — coordinates scrolling and takes screenshots

const MAX_SCREENSHOTS = 5; // Cap to keep cost and latency reasonable

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "captureFullPage") {
    captureFullPage()
      .then(result => sendResponse({ success: true, ...result }))
      .catch(err => sendResponse({ success: false, error: err.message }));
    return true; // keep channel open for async response
  }
});

async function captureFullPage() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  if (!tab) throw new Error("No active tab found.");

  // Freeze animations so screenshots are clean
  await chrome.tabs.sendMessage(tab.id, { action: "freezeAnimations" });

  // Get page dimensions
  const pageInfo = await chrome.tabs.sendMessage(tab.id, { action: "getPageHeight" });
  const { totalHeight, windowHeight } = pageInfo;

  // Calculate scroll steps — cap at MAX_SCREENSHOTS
  const totalSteps = Math.ceil(totalHeight / windowHeight);
  const steps = Math.min(totalSteps, MAX_SCREENSHOTS);

  const screenshots = [];
  const positions = [];

  for (let i = 0; i < steps; i++) {
    // Distribute evenly across the full page height
    const position = i === 0
      ? 0
      : Math.round((i / (steps - 1 || 1)) * (totalHeight - windowHeight));

    positions.push(position);

    // Scroll to position — longer wait for pages with lazy loading
    await chrome.tabs.sendMessage(tab.id, {
      action: "scrollTo",
      position,
      wait: 400,
    });

    await sleep(450); // Extra buffer after content.js confirms

    // Take screenshot
    const dataUrl = await chrome.tabs.captureVisibleTab(tab.windowId, {
      format: "jpeg",
      quality: 82,
    });

    screenshots.push(dataUrl);
  }

  // Restore page to top
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
