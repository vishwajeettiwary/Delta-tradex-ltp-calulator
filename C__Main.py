import os
import time
import threading
import datetime
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse

app = FastAPI(title="COA Option Chain Dynamic Engine")

# --- 1. सुपर डायनामिक फ़ाइल फाइंडर (Case, Space & Spelling Safe) ---
# यह फ़ंक्शन वर्तमान या भविष्य की किसी भी नई फ़ाइल को अपने-आप ढूँढ लेगा
def get_exact_filepath(requested_filename: str):
    # 1. अगर exact फ़ाइल मिल जाए
    if os.path.exists(requested_filename):
        return requested_filename
    
    # 2. अगर स्पेस या Capital/Small अक्षर की वजह से मैच न हो (e.g. 'app. Js' -> 'app.js')
    clean_requested = requested_filename.lower().replace(" ", "")
    
    try:
        for file in os.listdir("."):
            clean_file = file.lower().replace(" ", "")
            if clean_file == clean_requested:
                return file
    except Exception as e:
        print(f"File search warning: {e}")
        
    return None

# --- 2. BACKGROUND COA ENGINE LOOP ---
def run_option_chain_engine():
    print(f"[{datetime.datetime.now()}] 🚀 COA Engine Running in Background...")
    while True:
        try:
            pass
        except Exception as err:
            print(f"Engine Loop Warning: {err}")
        time.sleep(2)

@app.on_event("startup")
def start_background_loop():
    thread = threading.Thread(target=run_option_chain_engine, daemon=True)
    thread.start()

# --- 3. ROOT ROUTE '/' (ऑटोमैटिक डिफ़ॉल्ट होमपेज) ---
@app.get("/")
def serve_homepage():
    # सबसे पहले किसी भी प्रकार के index.html को ढूँढेगा
    index_file = get_exact_filepath("index.html")
    if index_file:
        return FileResponse(index_file)
    
    # अगर index.html न मिले तो फ़ोल्डर की पहली कोई भी .html फ़ाइल ऑटोमैटिक सर्व कर देगा
    for file in os.listdir("."):
        if file.lower().endswith(".html"):
            return FileResponse(file)
            
    return {"error": "कोई भी HTML फ़ाइल नहीं मिली!"}

# --- 4. UNIVERSAL CATCH-ALL ROUTE (भविष्य की सभी 100+ फ़ाइलों के लिए) ---
# अब तुम चाहे COA Phase 2, Phase 3, new_style.css, algo.js कुछ भी जोड़ो, 
# यह बिना Main.py बदले हर फ़ाइल को ऑटो-कनेक्ट कर देगा!
@app.get("/{file_name:path}")
def serve_any_project_file(file_name: str):
    exact_file = get_exact_filepath(file_name)
    
    if exact_file and os.path.isfile(exact_file):
        return FileResponse(exact_file)
    
    return Response(status_code=404, content=f"File '{file_name}' not found in repo.")
