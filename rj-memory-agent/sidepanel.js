// sidepanel.js

const MODEL      = "claude-sonnet-4-6";
const MAX_TOKENS = 1200;

// ── DOM refs ──────────────────────────────────────────────────────────────────
const scanBtn      = document.getElementById("scanBtn");
const stopBtn      = document.getElementById("stopBtn");
const questionEl   = document.getElementById("question");
const statusEl     = document.getElementById("status");
const stepsEl      = document.getElementById("steps");
const filmstrip    = document.getElementById("filmstrip");
const answerBox    = document.getElementById("answerBox");
const errorBox     = document.getElementById("errorBox");
const adminPanel   = document.getElementById("adminPanel");
const gearTrigger  = document.getElementById("gearTrigger");
const keyInput     = document.getElementById("keyInput");
const saveKeyBtn   = document.getElementById("saveKeyBtn");
const keyStatus    = document.getElementById("keyStatus");
const keyIndicator = document.getElementById("keyIndicator");

// ── Triple-click BETA badge → admin panel ─────────────────────────────────────
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

// ── Load saved API key ────────────────────────────────────────────────────────
chrome.storage.sync.get("apiKey", data => {
  if (data.apiKey) {
    keyInput.value = data.apiKey;
    keyStatus.classList.add("visible");
    keyIndicator.classList.add("visible");
  }
});

saveKeyBtn.addEventListener("click", () => {
  const key = keyInput.value.trim();
  if (!key) return;
  chrome.storage.sync.set({ apiKey: key }, () => {
    keyStatus.textContent = "✓ Key saved and active";
    keyStatus.classList.add("visible");
    keyIndicator.classList.add("visible");
    setTimeout(() => adminPanel.classList.remove("visible"), 1200);
  });
});

// ── Listen for live progress from background.js ───────────────────────────────
chrome.runtime.onMessage.addListener((message) => {
  if (message.action === "agentProgress") {
    addStep(message.step, message.status, message.detail);
  }
  if (message.action === "agentScreenshot") {
    addFilmstripFrame(message.data, message.label);
  }
});

// ── Main handler ──────────────────────────────────────────────────────────────
scanBtn.addEventListener("click", async () => {
  const question = questionEl.value.trim();
  if (!question) { showError("Please type a question first."); return; }

  const apiKey = await getStoredKey();
  if (!apiKey) {
    showError("No API key found. Triple-click the BETA badge to add one.");
    return;
  }

  reset();
  setBtn(true);
  stopBtn.style.display = "block";
  addStep(0, "🚀 Starting agent...");

  const result = await chrome.runtime.sendMessage({
    action: "startAgentLoop",
    question,
    apiKey,
  });

  stopBtn.style.display = "none";

  if (result?.success) {
    showAnswer(result.answer);
    setStatus(result.stopped ? "🛑 Stopped by user" : "✅ Done");
  } else {
    showError(result?.error || "Something went wrong.");
    setStatus("");
  }

  setBtn(false);
});

stopBtn.addEventListener("click", () => {
  chrome.runtime.sendMessage({ action: "stopAgentLoop" });
  stopBtn.style.display = "none";
  addStep(0, "🛑 Stopping after this step...");
});

// ── UI helpers ────────────────────────────────────────────────────────────────
function reset() {
  answerBox.innerHTML  = ""; answerBox.classList.remove("visible");
  errorBox.textContent = ""; errorBox.classList.remove("visible");
  stepsEl.innerHTML    = ""; stepsEl.classList.remove("visible");
  statusEl.textContent = "";
  filmstrip.innerHTML  = ""; filmstrip.classList.remove("visible");
}

function addFilmstripFrame(b64data, label) {
  filmstrip.classList.add("visible");
  const prev = filmstrip.querySelector(".filmstrip-frame.active");
  if (prev) prev.classList.remove("active");
  const frame = document.createElement("div");
  frame.className = "filmstrip-frame active";
  frame.innerHTML =
    `<img src="data:image/jpeg;base64,${b64data}" alt="screenshot"/>` +
    `<div class="filmstrip-label">${label}</div>`;
  filmstrip.appendChild(frame);
  frame.scrollIntoView({ behavior: "smooth", inline: "end" });
}

function setBtn(disabled) {
  scanBtn.disabled    = disabled;
  scanBtn.textContent = disabled ? "⏳ Agent working..." : "Ask";
}

function setStatus(msg) { statusEl.textContent = msg; }

function addStep(num, status = "", detail = "") {
  stepsEl.classList.add("visible");
  const row = document.createElement("div");
  row.className = "step-row";
  row.innerHTML =
    `<span class="step-status">${status}</span>` +
    (detail ? `<span class="step-detail">${detail}</span>` : "");
  stepsEl.appendChild(row);
  stepsEl.scrollTop = stepsEl.scrollHeight;
  statusEl.textContent = status;
}

function showAnswer(text) {
  if (!text) return;
  const html = text
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/^### (.+)$/gm, "<h4>$1</h4>")
    .replace(/^## (.+)$/gm,  "<h3>$1</h3>")
    .replace(/^- (.+)$/gm,   "<li>$1</li>")
    .replace(/(<li>.*<\/li>)/gs, "<ul>$1</ul>")
    .replace(/\n\n/g, "<br><br>")
    .replace(/\n/g, "<br>");
  answerBox.innerHTML = html;
  answerBox.classList.add("visible");
  setTimeout(() => answerBox.scrollIntoView({ behavior: "smooth", block: "start" }), 100);
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
