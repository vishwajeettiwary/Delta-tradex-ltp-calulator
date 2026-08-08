import datetime
from fyers_service import get_fyers_spot_price

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

def generate_coa_grid(symbol_key: str):
    sym = symbol_key.upper()
    cfg = SYMBOL_CONFIG.get(sym, SYMBOL_CONFIG["NIFTY"])
    step = cfg["step"]
    
    spot_price_raw, is_live = get_fyers_spot_price(cfg["symbol_code"])
    spot_price = float(spot_price_raw) if spot_price_raw else cfg["default_spot"]
    status_text = "LIVE REAL-TIME" if is_live else "MARKET DATA (OFFLINE)"

    lower_atm = int(spot_price // step) * step
    upper_atm = lower_atm + step

    strikes = [lower_atm - (i * step) for i in range(10, 0, -1)] + \
              [lower_atm, upper_atm] + \
              [upper_atm + (i * step) for i in range(1, 9)]

    raw_data = []
    total_ce_oi_sum, total_pe_oi_sum = 0, 0
    max_ce_oi, max_ce_vol, max_ce_oichg = 1, 1, 1
    max_pe_oi, max_pe_vol, max_pe_oichg = 1, 1, 1

    res_strike = lower_atm + step
    sup_strike = lower_atm - step

    for st in strikes:
        is_res = (st == res_strike)
        is_sup = (st == sup_strike)

        ce_oi = 150000 if is_res else (95000 if st == upper_atm else 30000 + (st % 1000))
        pe_oi = 165000 if is_sup else (85000 if st == lower_atm else 28000 + (st % 1000))
        ce_vol = int(ce_oi * 2.1)
        pe_vol = int(pe_oi * 2.1)
        ce_oichg = int(ce_oi * 0.12)
        pe_oichg = int(pe_oi * 0.15)

        total_ce_oi_sum += ce_oi
        total_pe_oi_sum += pe_oi

        if ce_oi > max_ce_oi: max_ce_oi = ce_oi
        if pe_oi > max_pe_oi: max_pe_oi = pe_oi
        if ce_vol > max_ce_vol: max_ce_vol = ce_vol
        if pe_vol > max_pe_vol: max_pe_vol = pe_vol
        if ce_oichg > max_ce_oichg: max_ce_oichg = ce_oichg
        if pe_oichg > max_pe_oichg: max_pe_oichg = pe_oichg

        raw_data.append({
            "st": st, "ce_oi": ce_oi, "pe_oi": pe_oi,
            "ce_vol": ce_vol, "pe_vol": pe_vol,
            "ce_oichg": ce_oichg, "pe_oichg": pe_oichg
        })

    overall_pcr = round(total_pe_oi_sum / total_ce_oi_sum, 2) if total_ce_oi_sum > 0 else 1.0
    rows_data = []
    now_str = datetime.datetime.now().strftime("%I:%M:%S %p")

    for idx, item in enumerate(raw_data, start=1):
        st = item["st"]

        ce_oi_pct = round((item["ce_oi"] / max_ce_oi) * 100, 1)
        pe_oi_pct = round((item["pe_oi"] / max_pe_oi) * 100, 1)
        ce_vol_pct = round((item["ce_vol"] / max_ce_vol) * 100, 1)
        pe_vol_pct = round((item["pe_vol"] / max_pe_vol) * 100, 1)
        ce_oichg_pct = round((item["ce_oichg"] / max_ce_oichg) * 100, 1)
        pe_oichg_pct = round((item["pe_oichg"] / max_pe_oichg) * 100, 1)

        ce_ltp = max(1.5, (spot_price - st) + 60.0) if st < spot_price else max(1.5, 100.0 - (st - spot_price) * 0.5)
        pe_ltp = max(1.5, (st - spot_price) + 60.0) if st > spot_price else max(1.5, 100.0 - (spot_price - st) * 0.5)

        rows_data.append({
            "row_number": idx,
            "is_row_13": (idx == 13),
            "is_ce_itm": st < spot_price,
            "is_pe_itm": st > spot_price,
            
            # CALL SIDE (Resistance) - Columns 1 to 6
            "col_1_ce_scenario": f"Bullish ➔ Neutral",
            "col_2_ce_shift": f"WTT Towards {res_strike + step}",
            "col_3_ce_oichg": f"{ce_oichg_pct}%",
            "col_4_ce_vol": f"{ce_vol_pct}%",
            "col_5_ce_oi": f"{ce_oi_pct}%",
            "col_6_ce_overall_res": f"₹{round(ce_ltp, 2)}",
            
            # CENTER Column 7
            "col_7_strike_or_spot": str(st),
            
            # PUT SIDE (Support) - Columns 8 to 13
            "col_8_pe_overall_sup": f"₹{round(pe_ltp, 2)}",
            "col_9_pe_oi": f"{pe_oi_pct}%",
            "col_10_pe_vol": f"{pe_vol_pct}%",
            "col_11_pe_oichg": f"{pe_oichg_pct}%",
            "col_12_pe_shift": f"Stable Support",
            "col_13_pe_scenario": f"Neutral ➔ Bullish"
        })

    # Row 13 Logic Override
    r13 = rows_data[12]
    r13["col_1_ce_scenario"] = f"Scenario 2 (Bullish) ➔ Scenario 1 (Strong Resistance) [{now_str}]"
    r13["col_2_ce_shift"] = f"Shifting: WTT Towards {res_strike + step} [{now_str}]"
    r13["col_3_ce_oichg"] = f"Call OI Chg Indiv Res: Strong at {res_strike} [{now_str}]"
    r13["col_4_ce_vol"] = f"Call Vol Indiv Res: WTT {res_strike + step} (85%) [{now_str}]"
    r13["col_5_ce_oi"] = f"Call OI Indiv Res: Strong at {res_strike} [{now_str}]"
    r13["col_6_ce_overall_res"] = f"Overall Resistance: Strong at {res_strike} [{now_str}]"
    
    r13["col_7_strike_or_spot"] = f"SPOT: {spot_price} | PCR: {overall_pcr}"
    
    r13["col_8_pe_overall_sup"] = f"Overall Support: Strong at {sup_strike} [{now_str}]"
    r13["col_9_pe_oi"] = f"Put OI Indiv Sup: Strong at {sup_strike} [{now_str}]"
    r13["col_10_pe_vol"] = f"Put Vol Indiv Sup: Strong at {sup_strike} [{now_str}]"
    r13["col_11_pe_oichg"] = f"Put OI Chg Indiv Sup: Strong at {sup_strike} [{now_str}]"
    r13["col_12_pe_shift"] = f"Shifting: Stable Support at {sup_strike} [{now_str}]"
    r13["col_13_pe_scenario"] = f"Scenario 1 (Neutral) ➔ Scenario 1 (Strong Support) [{now_str}]"

    return {
        "symbol": sym,
        "spot_price": spot_price,
        "overall_pcr": overall_pcr,
        "status_text": status_text,
        "last_update_time": now_str,
        "rows": rows_data
    }
