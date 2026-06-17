// background.js — true agentic loop with Claude tool use
const MAX_STEPS    = 10;
const AGENT_MODEL  = "claude-sonnet-4-6";
const AGENT_TOKENS = 1500;

let agentAbortController = null;
let agentShouldStop      = false;

chrome.action.onClicked.addListener(tab => {
  chrome.sidePanel.open({ tabId: tab.id });
});

// ── Message router ────────────────────────────────────────────────────────────
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "startAgentLoop") {
    agentShouldStop = false;
    runAgentLoop(message.question, message.apiKey)
      .then(result => sendResponse(result))
      .catch(err => {
        // Always clean up the overlay on any crash
        chrome.tabs.query({ active: true, currentWindow: true }, ([tab]) => {
          if (tab) {
            chrome.tabs.sendMessage(tab.id, { action: "hideAgentOverlay" }).catch(() => {});
            chrome.tabs.sendMessage(tab.id, { action: "unfreezeAnimations" }).catch(() => {});
          }
        });
        sendResponse({ success: false, error: err.message });
      });
    return true;
  }
  if (message.action === "stopAgentLoop") {
    agentShouldStop = true;
    if (agentAbortController) agentAbortController.abort();
  }
});

// Send live progress to the side panel
function sendProgress(step, status, detail = "") {
  chrome.runtime.sendMessage({ action: "agentProgress", step, status, detail }).catch(() => {});
}

// Send screenshot thumbnail to side panel for visual display
function sendScreenshot(dataB64, label) {
  chrome.runtime.sendMessage({ action: "agentScreenshot", data: dataB64, label }).catch(() => {});
}

// ── Agent loop ────────────────────────────────────────────────────────────────
async function runAgentLoop(question, apiKey) {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab) return { success: false, error: "No active tab found." };
  if (tab.url.startsWith("chrome://") || tab.url.startsWith("chrome-extension://")) {
    return { success: false, error: "Cannot scan Chrome internal pages. Navigate to a real webpage first." };
  }

  // Inject content script
  await chrome.scripting.executeScript({ target: { tabId: tab.id, allFrames: true }, files: ["content.js"] });
  await sleep(200);
  const ping = await safeSend(tab.id, { action: "ping" });
  if (!ping?.alive) return { success: false, error: "Could not connect to page. Try refreshing." };

  await chrome.tabs.sendMessage(tab.id, { action: "freezeAnimations" });
  await safeSend(tab.id, { action: "showAgentOverlay", label: "AI Agent is analyzing this page…" });

  const conversationMessages = [];
  let stepCount = 0;

  sendProgress(0, "🔍 Looking at the page...");

  // ── Tool definitions Claude can call ────────────────────────────────────────
  const tools = [
    {
      name: "scroll_down",
      description: "Scroll down to see more content below the current view. Use when you can see that content is cut off or there are more items below.",
      input_schema: { type: "object", properties: {}, required: [] },
    },
    {
      name: "scroll_to_top",
      description: "Scroll back to the top of the page.",
      input_schema: { type: "object", properties: {}, required: [] },
    },
    {
      name: "click_element",
      description: "Click a button, tab, or link on the page by its visible text label.",
      input_schema: {
        type: "object",
        properties: {
          text: { type: "string", description: "The visible text of the element to click, e.g. 'Memory Timeline' or 'Note Encoder'" },
        },
        required: ["text"],
      },
    },
    {
      name: "provide_final_answer",
      description: "Call this when you have gathered enough information to fully answer the advisor's question. Provide a complete, comprehensive response.",
      input_schema: {
        type: "object",
        properties: {
          answer: { type: "string", description: "The complete answer to the advisor's question" },
        },
        required: ["answer"],
      },
    },
  ];

  const systemPrompt =
    "You are an AI agent inside a Chrome extension helping a Raymond James financial advisor. " +
    "You can see screenshots of the page and take actions: scroll down, click tabs/buttons, or provide a final answer. " +
    "IMPORTANT: Always scroll down or click tabs to gather ALL relevant information before answering. " +
    "If you can see partial information (e.g. only some clients), scroll down to see the rest. " +
    "If there are tabs on the page (like 'Memory Timeline', 'Note Encoder'), click them if relevant to the question. " +
    "Only call provide_final_answer when you are confident you have seen everything needed. " +
    "Be thorough — a financial advisor's decisions depend on complete information.";

  // ── Main loop ────────────────────────────────────────────────────────────────
  while (stepCount < MAX_STEPS) {
    if (agentShouldStop) {
      await cleanup(tab.id);
      return { success: true, answer: "Agent stopped by user.", stopped: true };
    }
    stepCount++;

    // Take screenshot of current view
    const screenshot = await captureCurrentView(tab);
    const pageInfo   = await safeSend(tab.id, { action: "getPageHeight" }) || {};
    const scrollPct  = pageInfo.totalHeight > 0
      ? Math.round((pageInfo.scrollTop / Math.max(1, pageInfo.totalHeight - pageInfo.windowHeight)) * 100)
      : 0;

    // Send thumbnail to side panel for visual display
    sendScreenshot(screenshot, `Step ${stepCount} · ${scrollPct}%`);

    // Build user turn: screenshot + context
    const userContent = [
      {
        type: "image",
        source: { type: "base64", media_type: "image/jpeg", data: screenshot },
      },
      {
        type: "text",
        text: stepCount === 1
          ? `I am a Raymond James financial advisor. Here is a screenshot of the page I'm on.\n\nMy question: "${question}"\n\nPage context: ${pageInfo.totalHeight || "?"}px tall, currently at ${scrollPct}% scroll position.\n\nLook at everything visible. If you need more information to answer fully, use the tools to scroll or click. Only provide_final_answer when you have seen everything needed.`
          : `Here is the current state of the page (step ${stepCount}/${MAX_STEPS}, at ${scrollPct}% scroll). Continue gathering information or provide your final answer if you have enough.`,
      },
    ];

    conversationMessages.push({ role: "user", content: userContent });

    sendProgress(stepCount, `Agent is deciding what to do...`);
    await safeSend(tab.id, { action: "updateAgentOverlay", label: `AI Agent scanning…` });

    // Call Claude with tools
    let response;
    try {
      response = await callClaudeWithTools(apiKey, systemPrompt, conversationMessages, tools);
    } catch (err) {
      if (agentShouldStop) {
        await cleanup(tab.id);
        return { success: true, answer: "Agent stopped by user.", stopped: true };
      }
      if (err.name === "AbortError") {
        await cleanup(tab.id);
        return { success: false, error: "Request timed out. The page may be too complex or the API is slow. Please try again." };
      }
      throw err;
    }

    // Add assistant turn to conversation
    conversationMessages.push({ role: "assistant", content: response.content });

    // Find tool use in response
    const toolUse = response.content.find(c => c.type === "tool_use");
    const textBlock = response.content.find(c => c.type === "text");

    if (!toolUse) {
      await cleanup(tab.id);
      return { success: true, answer: textBlock?.text || "No answer generated." };
    }

    // ── Handle each tool ────────────────────────────────────────────────────
    if (toolUse.name === "provide_final_answer") {
      sendProgress(stepCount, "✅ Compiling answer...");
      await cleanup(tab.id);
      return { success: true, answer: toolUse.input.answer };
    }

    let toolResult = "";

    if (toolUse.name === "scroll_down") {
      sendProgress(stepCount, "⬇️ Scrolling down...");
      await safeSend(tab.id, { action: "updateAgentOverlay", label: "AI Agent scanning…", bar: "Scrolling down..." });
      const res = await safeSend(tab.id, { action: "scrollDown", wait: 600 });
      await sleep(700);
      toolResult = res?.atBottom
        ? "Scrolled down. Now at the bottom of the page."
        : "Scrolled down successfully. More content may be visible.";
    }

    if (toolUse.name === "scroll_to_top") {
      sendProgress(stepCount, "⬆️ Scrolling to top...");
      await safeSend(tab.id, { action: "scrollToTop" });
      await sleep(500);
      toolResult = "Scrolled back to top of page.";
    }

    if (toolUse.name === "click_element") {
      const text = toolUse.input.text;
      sendProgress(stepCount, `🖱️ Clicking "${text}"...`);
      await safeSend(tab.id, { action: "updateAgentOverlay", label: "AI Agent scanning…", bar: `Clicking "${text}"...` });
      const res = await safeSend(tab.id, { action: "clickElement", text });
      await sleep(900); // wait for page to update after click
      toolResult = res?.success
        ? `Successfully clicked "${res.clicked}". Page may have updated.`
        : `Could not find element "${text}". It may not be visible or may have a different label.`;
    }

    // Add tool result to conversation
    conversationMessages.push({
      role: "user",
      content: [{
        type: "tool_result",
        tool_use_id: toolUse.id,
        content: toolResult,
      }],
    });
  }

  await cleanup(tab.id);
  return { success: true, answer: "Reached maximum steps. Based on everything seen, here is my best answer — but consider scrolling through the full page manually for any details I may have missed." };
}

// ── Helpers ───────────────────────────────────────────────────────────────────
async function captureCurrentView(tab) {
  await sleep(150);
  const dataUrl = await chrome.tabs.captureVisibleTab(tab.windowId, { format: "jpeg", quality: 85 });
  return dataUrl.replace("data:image/jpeg;base64,", "");
}

async function callClaudeWithTools(apiKey, system, messages, tools) {
  agentAbortController = new AbortController();
  const timeout = setTimeout(() => agentAbortController.abort(), 60000);

  let response;
  try {
    response = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      signal: agentAbortController.signal,
      headers: {
        "Content-Type": "application/json",
        "x-api-key": apiKey,
        "anthropic-version": "2023-06-01",
        "anthropic-dangerous-direct-browser-access": "true",
      },
      body: JSON.stringify({
        model: AGENT_MODEL,
        max_tokens: AGENT_TOKENS,
        system,
        tools,
        messages,
      }),
    });
  } finally {
    clearTimeout(timeout);
    agentAbortController = null;
  }

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.error?.message || `API error ${response.status}`);
  }
  return response.json();
}

async function cleanup(tabId) {
  await safeSend(tabId, { action: "hideAgentOverlay" }).catch(() => {});
  await safeSend(tabId, { action: "unfreezeAnimations" }).catch(() => {});
}

function safeSend(tabId, message) {
  return new Promise(resolve => {
    chrome.tabs.sendMessage(tabId, message, response => {
      if (chrome.runtime.lastError) resolve(null);
      else resolve(response);
    });
  });
}

function sleep(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }
