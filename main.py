from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

API_KEY = os.getenv("API_KEY")
J.   J u.
@app.get("/", response_class=HTMLResponse)
async def root():
    return """ Cc
<!DOCTYPE html>
<html>
<head><title>HVACFlow</title><style>body{background:#000;color:#0f0;font-family:Arial;margin:0;padding:20px;}#chat{height:70vh;overflow:auto;border:1px solid #0f0;padding:10px;background:#111;border-radius:8px;}#input{width:100%;padding:12px;background:#111;color:#0f0;border:1px solid #0f0;margin-top:10px;border-radius:8px;}</style></head><body>
<h1>HVACFlow™</h1>
<div id="chat"></div>
<input id="input" placeholder="AC not cooling?">
<script>
const chat = document.getElementById('chat');
const input = document.getElementById('input');
async function ask(q) {
  const res = await fetch('/ask', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({q})});
  return (await res.json()).reply || 'Error';
}
input.onkeypress = async e => {
  if (e.key === 'Enter' && input.value.trim()) {
    const msg = input.value.trim();
    chat.innerHTML += `<p><b>You:</b> ${msg}</p><p><i>Thinking...</i></p>`;
    input.value = '';
    chat.scrollTop = chat.scrollHeight;
    const reply = await ask(msg);
    chat.lastChild.outerHTML = `<p><b>HVACFlow™:</b> ${reply}</p>`;
    chat.scrollTop = chat.scrollHeight;
  }
};
</script>
</body>
</html>
    """

@app.post("/ask")
async def ask(request: Request):
    try:
        data = await request.json()
        q = data.get("q", "")
    except:
        return {"reply": "Bad request"}
    if not q:
        return {"reply": "Type something"}
    if not API_KEY:
        return {"reply": "No API key"}
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            r = await client.post(
                "https://api.x.ai/v1/chat/completions",
                json={"model": "grok-beta", "messages": [{"role": "user", "content": q}], "max_tokens": 150},
                headers={"Authorization": f"Bearer {API_KEY}"}
            )
            if r.status_code == 200:
                return {"reply": r.json()["choices"][0]["message"]["content"]}
            return {"reply": f"API {r.status_code}"}
        except:
            return {"reply": "Service error"}
