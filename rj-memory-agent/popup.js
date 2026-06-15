// popup.js
// Handles UI interactions — sends messages to background.js, renders Claude's response

const ANTHROPIC_API_KEY = ""; // Set via chrome.storage or paste here for local testing
const MODEL = "claude-sonnet-4-6";
const MAX_TOKENS = 1200;

// ── DOM refs ──────────────────────────────────────────────────────────────────
const scanBtn     = document.getElementById("scanBtn");
const questionEl  = document.getElementById("question");
const statusEl    = document.getElementById("status");
const progressBar = document.getElementById("progressBar");
const progressFill = document.getElementById("progressFill");
const metaEl      = document.getElementById("meta");
const answerBox   = document.getElementById("answerBox");
const errorBox    = document.getElementById("errorBox");

// ── Main handler ──────────────────────────────────────────────────────────────
scanBtn.addEventListener("click", async () => {
  const question = questionEl.value.trim();
  if (!question) {
    showError("Please type a question first.");
    return;
  }

  reset();
  setBtn(true);
  setProgress(0);
  setStatus("📸 Scanning page...");

  try {
    // Step 1 — ask background.js to scroll and screenshot
    const result = await chrome.runtime.sendMessage({ action: "captureFullPage" });

    if (!result.success) throw new Error(result.error || "Screenshot failed.");

    const { screenshots, meta } = result;
    const count = screenshots.length;

    setProgress(40);
    setStatus(`✅ ${count} screenshot${count > 1 ? "s" : ""} captured. Asking Claude...`);

    if (meta.capped) {
      showMeta(`Page is ${meta.totalHeight}px tall — scanned ${count} sections (capped at ${count} to stay fast).`);
    } else {
      showMeta(`Scanned ${count} section${count > 1 ? "s" : ""} · ${meta.totalHeight}px page height`);
    }

    // Step 2 — build Claude message with all screenshots
    const imageBlocks = screenshots.map(dataUrl => ({
      type: "image",
      source: {
        type: "base64",
        media_type: "image/jpeg",
        data: dataUrl.replace("data:image/jpeg;base64,", ""),
      },
    }));

    imageBlocks.push({
      type: "text",
      text:
        `I am a Raymond James financial advisor. I have shared ${count} screenshot(s) ` +
        `of a client page, captured top to bottom in order.\n\n` +
        `Please read every screenshot carefully and answer this question:\n\n` +
        `"${question}"\n\n` +
        `Be specific. Use bullet points. Flag anything that needs immediate advisor attention.`,
    });

    setProgress(60);

    // Step 3 — call Claude API
    const apiKey = ANTHROPIC_API_KEY || await getStoredKey();
    if (!apiKey) throw new Error("No API key found. Add ANTHROPIC_API_KEY to popup.js or chrome.storage.");

    const response = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": apiKey,
        "anthropic-version": "2023-06-01",
        "anthropic-dangerous-direct-browser-usage": "true",
      },
      body: JSON.stringify({
        model: MODEL,
        max_tokens: MAX_TOKENS,
        system:
          "You are an AI assistant for Raymond James financial advisors. " +
          "You receive screenshots of client portfolio or CRM pages. " +
          "Identify risks, allocation mismatches, follow-up actions, and key insights. " +
          "Be concise. Lead with the most important finding. Use bullet points.",
        messages: [{ role: "user", content: imageBlocks }],
      }),
    });

    setProgress(90);

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.error?.message || `API error ${response.status}`);
    }

    const data = await response.json();
    const answer = data.content?.[0]?.text || "No response received.";

    setProgress(100);
    setStatus("✅ Done");
    showAnswer(answer);

  } catch (err) {
    setStatus("");
    showError(err.message);
  } finally {
    setBtn(false);
  }
});

// ── Helpers ───────────────────────────────────────────────────────────────────
function reset() {
  answerBox.textContent = "";
  answerBox.classList.remove("visible");
  errorBox.textContent = "";
  errorBox.classList.remove("visible");
  metaEl.textContent = "";
  metaEl.classList.remove("visible");
  progressBar.classList.remove("visible");
}

function setBtn(disabled) {
  scanBtn.disabled = disabled;
  scanBtn.textContent = disabled ? "⏳ Scanning..." : "📸 Scan Page & Ask Claude";
}

function setStatus(msg) {
  statusEl.textContent = msg;
}

function setProgress(pct) {
  progressBar.classList.add("visible");
  progressFill.style.width = pct + "%";
}

function showMeta(msg) {
  metaEl.textContent = msg;
  metaEl.classList.add("visible");
}

function showAnswer(text) {
  answerBox.textContent = text;
  answerBox.classList.add("visible");
}

function showError(msg) {
  errorBox.textContent = "⚠️ " + msg;
  errorBox.classList.add("visible");
}

async function getStoredKey() {
  return new Promise(resolve => {
    chrome.storage.sync.get("apiKey", data => resolve(data.apiKey || ""));
  });
}
