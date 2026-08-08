import os
import glob
import importlib.util
import datetime
import requests
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse

app = FastAPI(title="COA Master Multi-File Aggregator Engine")

# 1. आपकी सभी Python फाइलों को डायनामिकली ढूंढकर रन करने वाला लॉजिक
def run_all_repository_python_files(symbol_key: str):
    aggregated_results = {}
    
    # प्रोजेक्ट फ़ोल्डर की सभी .py फाइलें खोजें
    py_files = glob.glob("*.py")
    
    for file_path in py_files:
        filename = os.path.basename(file_path)
        module_name = filename.replace(".py", "").replace("-", "_")
        
        # main.py खुद को दोबारा न चलाए
        if module_name.lower() in ["main", "main_"]:
            continue
            
        try:
            # फाइल को डायनामिकली लोड/रजिस्टर करें
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            
            # अगर फाइल में कोई फंक्शन है तो उसे एग्जीक्यूट करें
            file_data = {}
            for attr in dir(mod):
                if not attr.startswith("__"):
                    obj = getattr(mod, attr)
                    if callable(obj):
                        try:
                            # अलग-अलग फाइलों के फंक्शन्स को ट्रिगर करें
                            file_data[attr] = str(obj(symbol_key)) if obj.__code__.co_argcount == 1 else str(obj())
                        except:
                            pass
                    elif isinstance(obj, (int, float, str, dict, list)):
                        file_data[attr] = obj
            
            aggregated_results[filename] = file_data
        except Exception as e:
            aggregated_results[filename] = {"status": "Loaded with notice", "info": str(e)}

    return aggregated_results

# 2. मेन Fyers और COA Grid लॉजिक (हर 1 सेकंड लाइव अपडेट)
FYERS_CLIENT_ID = os.environ.get("FYERS_CLIENT_ID", "J635Z4448N-100")
FYERS_ACCESS_TOKEN = os.environ.get("FYERS_ACCESS_TOKEN", "")

SYMBOL_CONFIG = {
    "NIFTY": {"symbol_code": "NSE:NIFTY50-INDEX", "step": 50, "default_spot": 24014.50},
    "SENSEX": {"symbol_code": "BSE:SENSEX-INDEX", "step": 100, "default_spot": 79500.00},
    "BANKNIFTY": {"symbol_code": "NSE:NIFTYBANK-INDEX", "step": 100, "default_spot": 51200.00},
    "BANKEX": {"symbol_code": "BSE:BANKEX-INDEX", "step": 100, "default_spot": 58100.00},
    "FINNIFTY": {"symbol_code": "NSE:FINNIFTY-INDEX", "step": 50, "default_spot": 23450.00},
    "MIDCPNIFTY": {"symbol_code": "NSE:MIDCPNIFTY-INDEX", "step": 25, "default_spot": 12300.00},
    "CRUDEOIL": {"symbol_code": "MCX:CRUDEOIL-MCX", "step": 50, "default_spot": 6450.00},
    "GOLD": {"symbol_code": "MCX:GOLD-MCX", "step": 100, "default_spot": 72100.00},
    "SILVER": {"symbol_code": "MCX:SILVER-MCX", "step": 500, "default_spot": 83500.00},
    "NATURALGAS": {"symbol_code": "MCX:NATURALGAS-MCX", "step": 5, "default_spot": 215.00}
}

def get_live_fyers_price(symbol_code: str):
    if not FYERS_ACCESS_TOKEN:
        return None, False
    try:
        headers = {"Authorization": f"{FYERS_CLIENT_ID}:{FYERS_ACCESS_TOKEN}"}
        url = f"https://api-v3.fyers.in/data/quotes?symbols={symbol_code}"
        res = requests.get(url, headers=headers, timeout=0.8)
        if res.status_code == 200:
            resp = res.json()
            if "d" in resp and len(resp["d"]) > 0:
                v = resp["d"][0]["v"]
                return v.get("lp") or v.get("cmd", {}).get("c"), True
    except: pass
    return None, False

def build_complete_master_data(symbol_key: str):
    sym = symbol_key.upper()
    cfg = SYMBOL_CONFIG.get(sym, SYMBOL_CONFIG["NIFTY"])
    step = cfg["step"]
    
    spot_raw, is_live = get_live_fyers_price(cfg["symbol_code"])
    spot_price = float(spot_raw) if spot_raw else cfg["default_spot"]
    
    lower_atm = int(spot_price // step) * step
    upper_atm = lower_atm + step
    strikes = [lower_atm - (i * step) for i in range(10, 0, -1)] + [lower_atm, upper_atm] + [upper_atm + (i * step) for i in range(1, 9)]

    rows_data = []
    now_str = datetime.datetime.now().strftime("%I:%M:%S %p")

    for idx, st in enumerate(strikes, start=1):
        ce_ltp = max(1.5, (spot_price - st) + 60.0) if st < spot_price else max(1.5, 100.0 - (st - spot_price) * 0.5)
        pe_ltp = max(1.5, (st - spot_price) + 60.0) if st > spot_price else max(1.5, 100.0 - (spot_price - st) * 0.5)
        
        rows_data.append({
            "is_row_13": (idx == 13),
            "col_1": "Bullish ➔ Neutral",
            "col_2": f"WTT Towards {lower_atm + step*2}",
            "col_3": f"{round((st%70)+12, 1)}%",
            "col_4": f"{round((st%85)+10, 1)}%",
            "col_5": f"{round((st%90)+5, 1)}%",
            "col_6": f"₹{round(ce_ltp, 2)}",
            "col_7": str(st),
            "col_8": f"₹{round(pe_ltp, 2)}",
            "col_9": f"{round((st%88)+6, 1)}%",
            "col_10": f"{round((st%80)+15, 1)}%",
            "col_11": f"{round((st%65)+18, 1)}%",
            "col_12": "Stable Support",
            "col_13": "Neutral ➔ Bullish"
        })

    # Row 13 Special Updates
    rows_data[12].update({
        "col_1": f"Resist at {lower_atm + step} [{now_str}]",
        "col_7": f"SPOT: {spot_price}",
        "col_13": f"Support at {lower_atm - step} [{now_str}]"
    })

    # बाकी सभी फाइलों का डेटा भी साथ में जोड़ें
    all_files_execution = run_all_repository_python_files(sym)

    return {
        "symbol": sym,
        "spot_price": spot_price,
        "status_text": "LIVE REAL-TIME" if is_live else "OFFLINE DATA",
        "last_update_time": now_str,
        "coa_rows": rows_data,
        "all_files_executed": list(all_files_execution.keys()),
        "all_files_output": all_files_execution
    }

@app.get("/api/option-chain")
def get_data(symbol: str = Query("NIFTY")):
    return JSONResponse(content=build_complete_master_data(symbol))

@app.get("/")
def serve_index():
    return FileResponse("index.html")
