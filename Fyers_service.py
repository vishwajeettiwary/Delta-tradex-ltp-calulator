import os
import requests

FYERS_CLIENT_ID = os.environ.get("FYERS_CLIENT_ID", "J635Z4448N-100")
FYERS_ACCESS_TOKEN = os.environ.get("FYERS_ACCESS_TOKEN", "")

def get_fyers_spot_price(symbol_code: str):
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
                last_price = v.get("lp") or v.get("cmd", {}).get("c")
                return last_price, True
    except Exception:
        pass
    return None, False
