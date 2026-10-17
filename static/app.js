const $ = (id) => document.getElementById(id);
const log = $("chatLog");
const promptBox = $("prompt");
const STORAGE_KEY = "athen-jarvis-history-v1";
let history = loadHistory();
let latestReply = "";
let toastTimer;

function loadHistory() {
  try {
    const value = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
    return Array.isArray(value) ? value : [];
  } catch { return []; }
}
function persistHistory() {
  history = history.slice(-60);
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(history)); } catch {}
}
function showToast(message) {
  const toast = $("toast");
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("show"), 3200);
}
function addMessage(role, text, save = true) {
  const wrapper = document.createElement("div");
  wrapper.className = `message ${role === "user" ? "user-message" : "assistant-message"}`;
  const icon = document.createElement("div");
  icon.className = "message-icon";
  icon.textContent = role === "user" ? "YOU" : "AJ";
  const body = document.createElement("div");
  const meta = document.createElement("div");
  meta.className = "message-meta";
  meta.textContent = role === "user" ? "YOU" : "ATHEN JARVIS";
  const time = document.createElement("span");
  time.textContent = new Date().toLocaleTimeString([], {hour: "2-digit", minute: "2-digit"});
  meta.append(time);
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;
  body.append(meta, bubble);
  wrapper.append(icon, body);
  log.append(wrapper);
  log.scrollTop = log.scrollHeight;
  if (save) { history.push({role, text, at: Date.now()}); persistHistory(); }
}
async function sendMessage(text) {
  const message = text.trim();
  if (!message) return;
  addMessage("user", message);
  promptBox.value = "";
  $("sendButton").disabled = true;
  $("systemStatus").textContent = "PROCESSING";
  const waiting = document.createElement("div");
  waiting.className = "message assistant-message";
  waiting.id = "thinking";
  const waitingText = document.createElement("div");
  waitingText.className = "bubble";
  waitingText.textContent = "Processing request...";
  const waitingBody = document.createElement("div");
  const waitingMeta = document.createElement("div");
  waitingMeta.className = "message-meta";
  waitingMeta.textContent = "ATHEN JARVIS";
  waitingBody.append(waitingMeta, waitingText);
  const waitingIcon = document.createElement("div");
  waitingIcon.className = "message-icon";
  waitingIcon.textContent = "AJ";
  waiting.append(waitingIcon, waitingBody);
  log.append(waiting);
  log.scrollTop = log.scrollHeight;
  try {
    const response = await fetch("/api/chat", {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message})});
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Assistant request failed.");
    latestReply = data.reply || "No response received.";
    $("thinking")?.remove();
    addMessage("assistant", latestReply);
    $("engineLabel").textContent = data.engine === "local" ? "OLLAMA LOCAL AI" : "OFFLINE FALLBACK";
    speak(latestReply, false);
  } catch (error) {
    $("thinking")?.remove();
    addMessage("assistant", `Connection error: ${error.message}. Is the backend running?`, false);
    showToast("Unable to reach the local assistant.");
  } finally {
    $("sendButton").disabled = false;
    $("systemStatus").textContent = "SYSTEM ONLINE";
    promptBox.focus();
  }
}
$("chatForm").addEventListener("submit", (event) => { event.preventDefault(); sendMessage(promptBox.value); });
promptBox.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) { event.preventDefault(); $("chatForm").requestSubmit(); }
});
async function runAction(action) {
  try {
    const response = await fetch("/api/action", {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({action})});
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Action was not allowed.");
    showToast(data.message);
    addMessage("assistant", data.message);
  } catch (error) { showToast(error.message); }
}
document.querySelectorAll("[data-action]").forEach((button) => button.addEventListener("click", () => runAction(button.dataset.action)));
function startVoiceInput() {
  const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!Recognition) { showToast("Speech recognition is not supported here. Try current Chrome or Edge."); return; }
  const recognition = new Recognition();
  recognition.lang = "en-US";
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;
  $("voiceButton").textContent = "LISTENING";
  $("voiceStatus").textContent = "LISTENING";
  recognition.onresult = (event) => {
    const spoken = event.results[0][0].transcript;
    promptBox.value = spoken;
    promptBox.focus();
    showToast(`Recognized: ${spoken}`);
  };
  recognition.onerror = (event) => showToast(`Voice input: ${event.error}`);
  recognition.onend = () => { $("voiceButton").textContent = "MIC"; $("voiceStatus").textContent = "STANDBY"; };
  try { recognition.start(); } catch { showToast("Microphone is already listening."); }
}
$("voiceButton").addEventListener("click", startVoiceInput);
function speak(text, announce = true) {
  if (!("speechSynthesis" in window)) { if (announce) showToast("Speech output is not supported in this browser."); return; }
  if (!text) { if (announce) showToast("Ask JARVIS a question first."); return; }
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "en-US"; utterance.rate = 1; utterance.pitch = 0.9;
  utterance.onstart = () => { $("voiceStatus").textContent = "SPEAKING"; };
  utterance.onend = () => { $("voiceStatus").textContent = "STANDBY"; };
  utterance.onerror = () => { $("voiceStatus").textContent = "STANDBY"; };
  window.speechSynthesis.speak(utterance);
  if (announce) showToast("Speaking latest assistant response.");
}
$("speakButton").addEventListener("click", () => speak(latestReply || [...history].reverse().find(x => x.role === "assistant")?.text, true));
$("stopButton").addEventListener("click", () => {
  if ("speechSynthesis" in window) window.speechSynthesis.cancel();
  $("voiceStatus").textContent = "STANDBY";
  showToast("Audio stopped.");
});
$("newChat").addEventListener("click", () => {
  log.replaceChildren(); latestReply = "";
  addMessage("assistant", "New session ready. All primary interface systems are online.", false);
  showToast("New session started. Saved history remains in this browser.");
});
function updateClock() { $("clock").textContent = new Date().toLocaleTimeString([], {hour12:false}); }
updateClock(); setInterval(updateClock, 1000);
async function checkHealth() {
  try {
    const response = await fetch("/api/health"); const data = await response.json();
    $("aiStatus").textContent = data.local_ai === "connected" ? "CONNECTED" : "FALLBACK";
    $("aiMeter").style.width = data.local_ai === "connected" ? "95%" : "38%";
    $("engineLabel").textContent = data.local_ai === "connected" ? `OLLAMA / ${data.model}` : "LOCAL FALLBACK";
  } catch { $("aiStatus").textContent = "OFFLINE"; $("aiMeter").style.width = "10%"; }
}
checkHealth();
history.slice(-18).forEach((item) => {
  addMessage(item.role, item.text, false);
  if (item.role === "assistant") latestReply = item.text;
});
