from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

app = FastAPI()

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
    }
    .user {
      align-self: flex-end;
      background-color: white;
      color: black;
      border-bottom-right-radius: 4px;
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
    }
    button {
      margin-left: 10px;
      padding: 10px 16px;
      background-color: #0078ff;
      color: white;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      font-size: 14px;
    }
    button:hover {
      background-color: #005fcc;
    }
  </style>
</head>
<body>
  <div id="header">💬 Psychological Pre-consultation Chatbot</div>
  <div id="chat-container"></div>
  <div id="input-container">
    <input type="text" id="user-input" placeholder="Type your message..." onkeydown="if(event.key==='Enter'){sendMessage();}"/>
    <button onclick="sendMessage()">Send</button>
  </div>

  <script>
    async function sendMessage() {
      const input = document.getElementById("user-input");
      const text = input.value.trim();
      if (!text) return;
      
      addMessage(text, "user");
      input.value = "";

      const response = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: text})
      });
      const data = await response.json();
      addMessage(data.reply, "bot");
    }

    function addMessage(text, sender) {
      const container = document.getElementById("chat-container");
      const div = document.createElement("div");
      div.className = "message " + sender;
      div.textContent = text;
      container.appendChild(div);
      container.scrollTop = container.scrollHeight;
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

@app.post("/chat", response_class=JSONResponse)
async def chat(req: ChatRequest):
    # Here you can hook up your moderation engine + model
    user_msg = req.message
    bot_reply = f"You said: {user_msg}"  # placeholder
    return {"reply": bot_reply}

# --- Run the app with: uvicorn app.app:app --reload ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
