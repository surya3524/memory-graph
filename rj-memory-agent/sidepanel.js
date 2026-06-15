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
    // ── PASS 1: Capture initial screenshot for Claude to assess ───────────────
    setStatus("📸 Taking initial screenshot...");
    const result = await chrome.runtime.sendMessage({ action: "captureFullPage" });
    if (!result.success) throw new Error(result.error || "Screenshot failed.");

    const { screenshots: pass1Screenshots, meta } = result;
    setProgress(25);
    showMeta(`Page: ${meta.totalHeight}px tall · ${meta.stepsUsed} section${meta.stepsUsed > 1 ? "s" : ""} captured`);

    // ── PASS 1 Claude call: assess what it sees and whether it needs more ─────
    setStatus("🤔 Claude is assessing the page...");
    const pass1Blocks = buildImageBlocks(pass1Screenshots);
    pass1Blocks.push({
      type: "text",
      text:
        `I am a Raymond James financial advisor. I need to answer this question:\n"${question}"\n\n` +
        `I have shared ${pass1Screenshots.length} screenshot(s) of the page taken top to bottom.\n\n` +
        `First, tell me in ONE sentence what you can see on this page.\n` +
        `Then, on a new line starting with NEEDS_MORE: answer YES or NO — do you need to see more of the page to fully answer my question? ` +
        `(Answer YES if the page appears cut off or if you can only see partial information relevant to the question.)\n` +
        `Then, on a new line starting with REASON: briefly explain why.`,
    });

    const assess = await callClaude(stored, pass1Blocks,
      "You are an AI page assessment assistant. Be brief and direct. Your job is to determine if you have enough visual information to answer the advisor's question.",
      300
    );

    setProgress(45);

    const needsMore = /NEEDS_MORE:\s*YES/i.test(assess);
    let allScreenshots = [...pass1Screenshots];

    // ── PASS 2: If Claude says it needs more, do a full scroll capture ────────
    if (needsMore && meta.totalHeight > meta.windowHeight + 100) {
      setStatus("🔍 Scrolling to capture full page...");
      const result2 = await chrome.runtime.sendMessage({ action: "captureFullPage" });
      if (result2.success) {
        allScreenshots = result2.screenshots;
        showMeta(`Full page captured · ${allScreenshots.length} sections · ${meta.totalHeight}px`);
      }
    }

    setProgress(65);
    setStatus(`📖 Reading ${allScreenshots.length} screenshot${allScreenshots.length > 1 ? "s" : ""}...`);

    // ── PASS 2 Claude call: answer the real question with all screenshots ──────
    const finalBlocks = buildImageBlocks(allScreenshots);
    finalBlocks.push({
      type: "text",
      text:
        `I am a Raymond James financial advisor. I have shared ${allScreenshots.length} screenshot(s) ` +
        `of a page, captured top to bottom (screenshot 1 = top, screenshot ${allScreenshots.length} = bottom).\n\n` +
        `Read ALL screenshots carefully — do not miss content from later screenshots.\n\n` +
        `Answer this question fully and specifically: "${question}"\n\n` +
        `Use bullet points. Lead with the most important finding. ` +
        `Flag anything needing immediate advisor attention.`,
    });

    const answer = await callClaude(stored, finalBlocks,
      "You are an AI assistant for Raymond James financial advisors. " +
      "You receive screenshots of client portfolio or CRM pages. " +
      "Read ALL screenshots before answering — content near the bottom is as important as the top. " +
      "Identify risks, allocation issues, and key actions. Be concise and use bullet points.",
      MAX_TOKENS
    );

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
  scanBtn.textContent = disabled ? "⏳ Thinking..." : "Ask";
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

function buildImageBlocks(screenshots) {
  return screenshots.map(dataUrl => ({
    type: "image",
    source: {
      type: "base64",
      media_type: "image/jpeg",
      data: dataUrl.replace("data:image/jpeg;base64,", ""),
    },
  }));
}

async function callClaude(apiKey, contentBlocks, system, maxTokens) {
  const response = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": apiKey,
      "anthropic-version": "2023-06-01",
      "anthropic-dangerous-direct-browser-access": "true",
    },
    body: JSON.stringify({
      model: MODEL,
      max_tokens: maxTokens,
      system,
      messages: [{ role: "user", content: contentBlocks }],
    }),
  });
  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.error?.message || `API error ${response.status}`);
  }
  const data = await response.json();
  return data.content?.[0]?.text || "No response received.";
}
