import importlib
import os
import threading
from flask import Flask, render_template_string, request

app = Flask(__name__)

# -------------------------------------------------------------
# 1. HTML Frontend (डैशबोर्ड और फ्लोटिंग AI CEO चैट)
# -------------------------------------------------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI CEO Master Dashboard</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }
        .dashboard-header { text-align: center; padding: 20px; background: #1e293b; border-radius: 12px; margin-bottom: 20px; border: 1px solid #334155; }
        .dashboard-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .card { background: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #334155; }
        
        /* Floating AI CEO Chat Widget */
        #ai-ceo-floating { position: fixed; bottom: 20px; right: 20px; width: 350px; background: #1e293b; border: 2px solid #3b82f6; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); overflow: hidden; }
        .chat-header { background: #2563eb; color: white; padding: 12px; font-weight: bold; display: flex; justify-content: space-between; align-items: center; }
        .chat-body { height: 300px; padding: 10px; overflow-y: auto; display: flex; flex-direction: column; gap: 8px; background: #0f172a; }
        .msg { padding: 8px 12px; border-radius: 8px; max-width: 80%; font-size: 14px; }
        .msg.user { background: #2563eb; color: white; align-self: flex-end; }
        .msg.ceo { background: #334155; color: white; align-self: flex-start; }
        .chat-input { display: flex; border-top: 1px solid #334155; }
        .chat-input input { flex: 1; padding: 10px; border: none; background: #1e293b; color: white; outline: none; }
        .chat-input button { padding: 10px 15px; background: #2563eb; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>

    <div class="dashboard-header">
        <h1>👑 Master AI CEO Control Panel</h1>
        <p>Status: <span style="color: #4ade80;">● Live 24/7 (Telegram & Web Connected)</span></p>
    </div>

    <div class="dashboard-grid">
        <div class="card">
            <h3>📈 Live Market Overview</h3>
            <p style="color: #94a3b8;">(चार्ट्स और ऑप्शन चैन यहाँ लोड होंगे)</p>
        </div>
        <div class="card">
            <h3>🤖 AI CEO System Health</h3>
            <p style="color: #94a3b8;">Telegram Listener: Active<br>Voice AI Processing: Ready</p>
        </div>
    </div>

    <!-- Floating AI CEO Chatbox -->
    <div id="ai-ceo-floating">
        <div class="chat-header">
            <span>💬 Floating AI CEO</span>
        </div>
        <div class="chat-body" id="chatBody">
            <div class="msg ceo">नमस्ते सर! मैं आपकी AI CEO हूँ। मैं Telegram और यहाँ दोनों जगह Live हूँ।</div>
        </div>
        <div class="chat-input">
            <input type="text" id="userInput" placeholder="कमांड टाइप करें..." onkeypress="if(event.key==='Enter') sendMsg()">
            <button onclick="sendMsg()">भेजें</button>
        </div>
    </div>

    <script>
        function sendMsg() {
            let input = document.getElementById('userInput');
            let text = input.value.trim();
            if(!text) return;
            
            let body = document.getElementById('chatBody');
            body.innerHTML += `<div class="msg user">${text}</div>`;
            input.value = '';
            
            // AI CEO का ऑटो रिप्लाई
            setTimeout(() => {
                body.innerHTML += `<div class="msg ceo">जी सर, आपकी कमांड "${text}" मुझे मिल गई है। मैं इस पर काम कर रही हूँ।</div>`;
                body.scrollTop = body.scrollHeight;
            }, 600);
        }
    </script>
</body>
</html>
"""


@app.route('/')
def home():
  return render_template_string(HTML_TEMPLATE)


# -------------------------------------------------------------
# 2. आपके 'ceo_main.py' को बैकग्राउंड में चालू रखना
# -------------------------------------------------------------
def start_ceo_main():
  try:
    print('🚀 Starting Telegram AI CEO from ceo_main.py...')
    # आपकी ceo_main.py फ़ाइल को बिना छेड़े लोड और रन करेगा
    importlib.import_module('ceo_main')
  except Exception as e:
    print(f'❌ Error running ceo_main: {e}')


# बैकग्राउंड थ्रेड में Telegram बोट चालू करें
threading.Thread(target=start_ceo_main, daemon=True).start()

# -------------------------------------------------------------
# 3. Web Server Port (रेंडर को ज़िंदा रखने के लिए)
# -------------------------------------------------------------
if __name__ == '__main__':
  port = int(os.environ.get('PORT', 10000))
  app.run(host='0.0.0.0', port=port)
