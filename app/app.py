import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from src.chat_engine import get_engine

app = FastAPI()
engine = get_engine()
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- HTML Template (chat window only) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Chatbot</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      height: 100vh;
      display: flex;
      flex-direction: column;
      background-color: #E0E0E0;
    }
    #header {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      background-color: #38404B;
      color: white;
      padding: 14px 20px;
      font-size: 18px;
      font-weight: bold;
      text-align: center;
      border-bottom: 1px solid #005fcc;
      z-index: 1000;
    }
    #chat-container {
      flex: 1;
      overflow-y: auto;
      padding: 80px 20px 20px; /* top padding = header height + space */
      display: flex;
      flex-direction: column;
    }
    .message {
      max-width: 70%;
      margin-bottom: 12px;
      padding: 10px 14px;
      border-radius: 12px;
      line-height: 1.4;
      word-wrap: break-word;
      white-space: pre-wrap;
    }
    .user {
      align-self: flex-end;
      background-color: white;
      color: black;
      border-bottom-right-radius: 4px;
      white-space: pre-wrap;
    }
    .bot {
      align-self: flex-start;
      background-color: #38404B;
      color: white;
      border-bottom-left-radius: 4px;
    }
    #input-container {
      display: flex;
      padding: 12px;
      border-top: 1px solid #ddd;
      background: white;
    }
    #user-input {
      flex: 1;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 8px;
      font-size: 14px;
      line-height: 20px;
      resize: none;          /* disable manual resize */
      overflow-y: hidden;    /* hide scroll initially */
      max-height: 100px;     /* limit max height */
    }
    button {
      margin-left: 10px;
      padding: 10px 16px;
      background-color: #8B9B97;
      color: white;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      font-size: 14px;
    }
    button:hover {
      background-color: #8B9B97;
    }

    /* Loading indicator styles */
    .loading-indicator {
      line-height: 1.4;
      display: inline-block;
      background-color: #38404B;
      padding: 10px 14px;
      border-radius: 8px;
      margin: 6px 0;
      align-self: flex-start;  /* left side like bot */
    }
    .loading-dots {
      display: flex;
      gap: 8px;
      align-items: center;
      justify-content: center;
    }

    .loading-dots span {
      width: 12px;
      height: 12px;
      background-color: white;
      border-radius: 50%;
      display: inline-block;
      animation: blink 1.2s ease-in-out infinite;
    }

    .loading-dots span:nth-child(2) { animation-delay: 0.2s; }
    .loading-dots span:nth-child(3) { animation-delay: 0.4s; }

    @keyframes blink {
      0%, 80%, 100% { opacity: 0; }
      40% { opacity: 1; }
    }
  </style>
</head>
<body>
  <div id="header">💬 Psychological Pre-consultation Chatbot</div>
  <div id="chat-container"></div>
  <div id="input-container">
    <textarea id="user-input" placeholder="Type your message..." rows="1"></textarea>
    <button onclick="sendMessage()">Send</button>
  </div>

  <script>
    const input = document.getElementById("user-input");
    const container = document.getElementById("chat-container");

    function adjustInputHeight() {
      input.style.height = "auto"; // Reset height
      const maxHeight = 100;
      if (input.scrollHeight > maxHeight) {
        input.style.height = maxHeight + "px";
        input.style.overflowY = "scroll"; // Enable scroll if exceeds max
      } else {
        input.style.height = input.scrollHeight + "px"; // Set to scrollHeight
        input.style.overflowY = "hidden"; // Hide scroll
      }
    }
    input.addEventListener("input", adjustInputHeight);

    async function sendMessage() {
      const input = document.getElementById("user-input");
      const text = input.value.trim();
      if (!text) return;
      
      addMessage(text, "user");
      input.value = "";
      adjustInputHeight();
      showLoading();

      try {
        const response = await fetch("/chat", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({message: text})
        });
        const data = await response.json();
        hideLoading();
        addMessage(data.reply, "bot");
      } catch (error) {
        hideLoading();
        addMessage("Error: Could not reach server.", "bot");
        console.error("Error:", error);
      }
    }

    // Enter to send, Shift+Enter for newline
    input.addEventListener('keydown', (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Keep input height if user clicks outside
    document.addEventListener('click', (e) => {
      if (!input.contains(e.target)) {
        if (!input.value.trim()) {
          input.style.height = 'auto'; // shrink back if empty
        } else {
          adjustInputHeight(); // keep height if has content
        }
      }
    });

    function addMessage(text, sender) {
      const container = document.getElementById("chat-container");
      const div = document.createElement("div");
      div.className = "message " + sender;
      div.textContent = text;
      container.appendChild(div);
      container.scrollTop = container.scrollHeight;
    }

    async function loadDisclaimer() {
      const response = await fetch("/disclaimer");
      const data = await response.json();
      if (data.disclaimer) {
        addMessage(data.disclaimer, "bot");
      }
    }
    window.onload = loadDisclaimer;

    function showLoading() {
      const loadingDiv = document.createElement('div');
      loadingDiv.id = 'loading-indicator';
      loadingDiv.className = 'loading-indicator';
      loadingDiv.innerHTML = `
        <div class="loading-dots">
            <span></span><span></span><span></span>
        </div>
      `;
      container.appendChild(loadingDiv);
      container.scrollTop = container.scrollHeight;
    }

    function hideLoading() {
      const loadingIndicator = document.getElementById('loading-indicator');
      if (loadingIndicator) loadingIndicator.remove();
    }
  </script>
</body>
</html>
"""


# --- API Models ---
class ChatRequest(BaseModel):
    message: str

# --- Routes ---
@app.get("/", response_class=HTMLResponse)
async def get_chat():
    return HTML_TEMPLATE

@app.route("/disclaimer")
async def disclaimer(req: ChatRequest):
    try:
        text = engine.moderator.get_disclaimer()
        return JSONResponse(content={"disclaimer": text})
    except Exception as e:
        logger.exception(f"Error getting disclaimer: {e}")
        return JSONResponse(
            status_code=500,
            content={"disclaimer": "Error fetching disclaimer."}
        )

@app.post("/chat", response_class=JSONResponse)
async def chat(req: ChatRequest):
    # Here you can hook up your moderation engine + model
    user_msg = req.message

    # Process message through chat engine
    result = engine.process_message(user_input=user_msg, include_context=True)

    # Extract the final response text
    bot_reply = result.get("response", "Sorry, something went wrong.")

    return {"reply": bot_reply}

# --- Run the app with: uvicorn app.app:app --reload ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
