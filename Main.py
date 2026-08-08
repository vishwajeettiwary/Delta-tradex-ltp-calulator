import os
import time
import threading
import datetime
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse

app = FastAPI(title="COA Option Chain Master Dashboard")

# --- 1. केस-इन्सेन्सिटिव फ़ाइल सर्च इंजन ---
# यह फ़ंक्शन Capital/Small अक्षर का फ़र्क मिटाकर आपके GitHub की सही फ़ाइल ढूँढ निकालेगा
def get_exact_filepath(requested_filename: str):
    if os.path.exists(requested_filename):
        return requested_filename
    
    # पूरे फ़ोल्डर में खोजें (Case-insensitive check)
    current_files = os.listdir(".")
    for file in current_files:
        if file.lower() == requested_filename.lower():
            return file
    return None

# --- 2. बैकग्राउंड डेटा इंजन ---
def run_option_chain_engine():
    print(f"[{datetime.datetime.now()}] 🚀 COA Engine Loop Running...")
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

# --- 3. मेन होमपेज (Root Path '/') ---
@app.get("/")
def serve_homepage():
    # आपकी रिपॉजिटरी में जो भी मुख्य HTML फ़ाइल मौजूद होगी, उसे लोड कर देगा
    for possible_name in ["index.html", "Index.Html", "Index.html", "Coa_phase1_engine.html"]:
        exact_file = get_exact_filepath(possible_name)
        if exact_file:
            return FileResponse(exact_file)
            
    return {"error": "कोई भी HTML फ़ाइल नहीं मिली!"}

# --- 4. स्मार्ट राउटर (यह आपकी हर CSS, JS और अन्य फ़ाइल को कनेक्ट करेगा) ---
@app.get("/{file_name:path}")
def serve_any_project_file(file_name: str):
    exact_file = get_exact_filepath(file_name)
    
    if exact_file and os.path.isfile(exact_file):
        return FileResponse(exact_file)
    
    return Response(status_code=404, content=f"File '{file_name}' not found in directory.")
