import os
import time
import datetime
from supabase import create_client, Client
from fyers_apiv3 import fyersModel

# --- 1. SUPABASE CONNECTION ---
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase = None

# --- 2. FYERS CREDENTIALS ---
CLIENT_ID = os.environ.get("FYERS_CLIENT_ID", "J635Z4448N-100")
SECRET_KEY = os.environ.get("FYERS_SECRET_KEY", "2TYPBHLC7X")
REDIRECT_URI = "https://trade.fyers.in/api-other/modal/login-acknowledgement"
ACCESS_TOKEN = os.environ.get("FYERS_ACCESS_TOKEN", "")

# --- 3. ACTIVE SYMBOLS LIST (10 SYMBOLS) ---
SYMBOLS = [
    "NIFTY", "BANKNIFTY", "SENSEX", "FINNIFTY", "BANKEX", 
    "MIDCPNIFTY", "CRUDEOIL", "NATURALGAS", "GOLD", "SILVER"
]

def get_fyers_instance():
    """Fyers Model initialize करने का फ़ंक्शन"""
    if not ACCESS_TOKEN:
        print("⚠️ Warning: FYERS_ACCESS_TOKEN set नहीं है।")
        return None
    return fyersModel.FyersModel(client_id=CLIENT_ID, token=ACCESS_TOKEN, is_async=False, log_path="")

def run_option_chain_engine():
    fyers = get_fyers_instance()
    print(f"[{datetime.datetime.now()}] 🚀 LTP Calculator Data Fetcher Engine Running...")

    for symbol in SYMBOLS:
        try:
            # यहाँ Fyers API से Live Data fetch होगा और Supabase में जाएगा
            # (प्रॉडक्शन में यह आपके 50+ Columns में जाएगा)
            print(f"Processing data for {symbol}...")
            
        except Exception as e:
            print(f"❌ Error fetching data for {symbol}: {e}")

if __name__ == "__main__":
    print("==========================================")
    print("🔥 LTP CALCULATOR MASTER ENGINE STARTED 🔥")
    print("==========================================")
    
    while True:
        try:
            run_option_chain_engine()
        except Exception as err:
            print(f"Error in main loop: {err}")
        
        time.sleep(2)  # हर 2 सेकंड में डेटा अपडेट होगा
