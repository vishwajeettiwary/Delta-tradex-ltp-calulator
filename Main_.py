import os
from fastapi import FastAPI, Response, Query
from fastapi.responses import FileResponse, JSONResponse
from coa_engine import generate_coa_grid

app = FastAPI(title="COA Modular Engine")

def get_exact_filepath(requested_filename: str):
    if os.path.exists(requested_filename):
        return requested_filename
    clean_req = requested_filename.lower().replace(" ", "")
    try:
        for file in os.listdir("."):
            if file.lower().replace(" ", "") == clean_req:
                return file
    except Exception:
        pass
    return None

@app.get("/api/option-chain")
def get_data(symbol: str = Query("NIFTY")):
    return JSONResponse(content=generate_coa_grid(symbol))

@app.get("/")
def serve_index():
    f = get_exact_filepath("index.html")
    if f:
        return FileResponse(f)
    return {"error": "index.html file missing"}

@app.get("/{file_name:path}")
def serve_file(file_name: str):
    f = get_exact_filepath(file_name)
    if f and os.path.isfile(f):
        return FileResponse(f)
    return Response(status_code=404)
