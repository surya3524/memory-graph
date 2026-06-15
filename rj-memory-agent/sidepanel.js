// sidepanel.js

const MODEL      = "claude-sonnet-4-6";
const MAX_TOKENS = 1200;

// ── DOM refs ──────────────────────────────────────────────────────────────────
const scanBtn      = document.getElementById("scanBtn");
const questionEl   = document.getElementById("question");
const statusEl     = document.getElementById("status");
const progressBar  = document.getElementById("progressBar");
const progressFill = document.getElementById("progressFill");
const metaEl       = document.getElementById("meta");
const answerBox    = document.getElementById("answerBox");
const errorBox     = document.getElementById("errorBox");
const adminPanel   = document.getElementById("adminPanel");
const gearTrigger  = document.getElementById("gearTrigger");
const keyInput     = document.getElementById("keyInput");
const saveKeyBtn   = document.getElementById("saveKeyBtn");
const keyStatus    = document.getElementById("keyStatus");
const keyIndicator = document.getElementById("keyIndicator");

// ── Triple-click gear → toggle admin panel ────────────────────────────────────
let gearClicks = 0, gearTimer = null;
gearTrigger.addEventListener("click", () => {
  gearClicks++;
  clearTimeout(gearTimer);
  gearTimer = setTimeout(() => { gearClicks = 0; }, 600);
  if (gearClicks >= 3) {
    gearClicks = 0;
    adminPanel.classList.toggle("visible");
  }
});

// ── Load saved key on open ────────────────────────────────────────────────────
chrome.storage.sync.get("apiKey", data => {
  if (data.apiKey) {
    keyInput.value = data.apiKey;
    keyStatus.classList.add("visible");
    keyIndicator.classList.add("visible"); // subtle green dot for developer
  }
});

// ── Save key ──────────────────────────────────────────────────────────────────
saveKeyBtn.addEventListener("click", () => {
  const key = keyInput.value.trim();
  if (!key) return;
  chrome.storage.sync.set({ apiKey: key }, () => {
    keyStatus.textContent = "✓ Key saved and active";
    keyStatus.classList.add("visible");
    keyIndicator.classList.add("visible");
    // Close admin panel after saving so demo viewers don't see it
    setTimeout(() => adminPanel.classList.remove("visible"), 1200);
  });
});

// ── Main scan handler ─────────────────────────────────────────────────────────
scanBtn.addEventListener("click", async () => {
  const question = questionEl.value.trim();
  if (!question) { showError("Please type a question first."); return; }

  const stored = await getStoredKey();
  if (!stored) {
    showError("No API key found. Triple-click the top-right corner of the header to add one.");
    return;
  }

  reset();
  setBtn(true);
  setProgress(5);
  setStatus("📸 Scanning page...");

  try {
    // Step 1 — background.js injects content.js, scrolls, screenshots
    const result = await chrome.runtime.sendMessage({ action: "captureFullPage" });
    if (!result.success) throw new Error(result.error || "Screenshot failed.");

    const { screenshots, meta } = result;
    const count = screenshots.length;

    setProgress(40);
    setStatus(`✅ ${count} screenshot${count > 1 ? "s" : ""} captured. Asking Claude...`);
    showMeta(
      meta.capped
        ? `Page is ${meta.totalHeight}px — captured ${count} sections (capped at ${count}).`
        : `Captured ${count} section${count > 1 ? "s" : ""} · ${meta.totalHeight}px page height`
    );

    // Step 2 — build Claude message with all screenshots in order
    const imageBlocks = screenshots.map((dataUrl, i) => ({
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
        `of a client page, captured top to bottom in order (screenshot 1 = top of page, ` +
        `screenshot ${count} = bottom of page).\n\n` +
        `Please read ALL screenshots carefully before answering. Do not miss content ` +
        `from later screenshots.\n\n` +
        `Question: "${question}"\n\n` +
        `Be specific. Use bullet points. Flag anything needing immediate advisor attention.`,
    });

    setProgress(65);

    // Step 3 — call Claude API
    const response = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": stored,
        "anthropic-version": "2023-06-01",
        "anthropic-dangerous-direct-browser-access": "true",
      },
      body: JSON.stringify({
        model: MODEL,
        max_tokens: MAX_TOKENS,
        system:
          "You are an AI assistant for Raymond James financial advisors. " +
          "You receive multiple screenshots of a client page taken top to bottom. " +
          "Read ALL screenshots — content in later screenshots is just as important. " +
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

    const data   = await response.json();
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
  answerBox.textContent = ""; answerBox.classList.remove("visible");
  errorBox.textContent  = ""; errorBox.classList.remove("visible");
  metaEl.textContent    = ""; metaEl.classList.remove("visible");
  progressBar.classList.remove("visible");
}

function setBtn(disabled) {
  scanBtn.disabled    = disabled;
  scanBtn.textContent = disabled ? "⏳ Scanning..." : "📸 Scan Page & Ask Claude";
}

function setStatus(msg) { statusEl.textContent = msg; }

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

function getStoredKey() {
  return new Promise(resolve => {
    chrome.storage.sync.get("apiKey", data => resolve(data.apiKey || ""));
  });
}
