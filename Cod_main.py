<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <title>COA Exact Analytics Grid</title>
    <style>
        body { background: #090c10; color: #f0f6fc; font-family: 'Segoe UI', monospace; padding: 10px; margin: 0; }
        .bar { display: flex; justify-content: space-between; align-items: center; background: #161b22; padding: 10px; border-radius: 6px; margin-bottom: 8px; border: 1px solid #30363d; }
        select { background: #21262d; color: #58a6ff; font-weight: bold; padding: 6px 12px; border: 1px solid #30363d; border-radius: 4px; }
        .table-container { overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; font-size: 11px; text-align: center; }
        th, td { border: 1px solid #30363d; padding: 6px 3px; white-space: nowrap; }
        th { background: #161b22; color: #58a6ff; }

        /* ITM & OTM Color Coding */
        .ce-itm { background: rgba(30, 70, 32, 0.35) !important; }
        .pe-itm { background: rgba(80, 30, 30, 0.35) !important; }

        /* Row 13 Special Analytics Highlighting */
        .row-13-style { background: #121d2b !important; border-top: 3px solid #f0883e !important; border-bottom: 3px solid #f0883e !important; font-weight: bold; }
        .row-13-style td { padding: 8px 3px; font-size: 11px; }

        .spot-center-box { background: #f0883e !important; color: #000 !important; font-weight: bold; font-size: 12px; }
    </style>
</head>
<body>

    <div class="bar">
        <div>
            <label style="font-weight:bold; color:#58a6ff;">SYMBOL: </label>
            <select id="symSelect" onchange="loadCoaGrid()">
                <option value="NIFTY">NIFTY</option>
                <option value="SENSEX">SENSEX</option>
                <option value="BANKNIFTY">BANKNIFTY</option>
                <option value="BANKEX">BANKEX</option>
                <option value="FINNIFTY">FINNIFTY</option>
                <option value="MIDCPNIFTY">MIDCPNIFTY</option>
                <option value="CRUDEOIL">CRUDEOIL</option>
                <option value="GOLD">GOLD</option>
                <option value="SILVER">SILVER</option>
                <option value="NATURALGAS">NATURALGAS</option>
            </select>
        </div>
        <div>
            <span id="pcrTag" style="background:#238636; color:#fff; padding:4px 8px; font-weight:bold; border-radius:4px; margin-right:10px;">PCR: -</span>
            <span id="statusTag" style="background:#f0883e; color:#000; padding:4px 8px; font-weight:bold; border-radius:4px;">STATUS</span>
            <span id="timeTag" style="color:#8b949e; margin-left:10px;">-</span>
        </div>
    </div>

    <div class="table-container">
        <table>
            <thead>
                <tr>
                    <th colspan="6" style="background:#0d3880; color:#fff;">CALL SIDE (COLUMNS 1 TO 6)</th>
                    <th style="background:#161b22; color:#f0883e;">COL 7</th>
                    <th colspan="6" style="background:#0e5229; color:#fff;">PUT SIDE (COLUMNS 8 TO 13)</th>
                </tr>
                <tr>
                    <th>Col 1<br>CE Scenario</th>
                    <th>Col 2<br>CE Shiftings</th>
                    <th>Col 3<br>CE OI Indiv</th>
                    <th>Col 4<br>CE Vol Indiv</th>
                    <th>Col 5<br>CE ChgOI Indiv</th>
                    <th>Col 6<br>CE Overall Res</th>
                    <th style="background:#f0883e; color:#000;">STRIKE / SPOT + PCR</th>
                    <th>Col 8<br>PE Overall Sup</th>
                    <th>Col 9<br>PE ChgOI Indiv</th>
                    <th>Col 10<br>PE Vol Indiv</th>
                    <th>Col 11<br>PE OI Indiv</th>
                    <th>Col 12<br>PE Shiftings</th>
                    <th>Col 13<br>PE Scenario</th>
                </tr>
            </thead>
            <tbody id="gridBody"></tbody>
        </table>
    </div>

    <script>
        async function loadCoaGrid() {
            const sym = document.getElementById("symSelect").value;
            const res = await fetch(`/api/option-chain?symbol=${sym}`);
            const data = await res.json();

            document.getElementById("pcrTag").innerText = "OVERALL PCR: " + data.overall_pcr;
            document.getElementById("statusTag").innerText = data.status_text;
            document.getElementById("timeTag").innerText = "Updated: " + data.last_update_time;

            const tbody = document.getElementById("gridBody");
            let html = "";

            data.rows.forEach(r => {
                const isR13 = r.is_row_13;
                const rowClass = isR13 ? "row-13-style" : "";

                html += `<tr class="${rowClass}">
                    <td class="${!isR13 && r.is_ce_itm ? 'ce-itm' : ''}" style="${isR13 ? 'color:#ff7b72;' : ''}">${r.col_1_ce_oi}</td>
                    <td class="${!isR13 && r.is_ce_itm ? 'ce-itm' : ''}" style="${isR13 ? 'color:#d29922;' : ''}">${r.col_2_ce_oichg}</td>
                    <td class="${!isR13 && r.is_ce_itm ? 'ce-itm' : ''}" style="${isR13 ? 'color:#58a6ff;' : ''}">${r.col_3_ce_vol}</td>
                    <td class="${!isR13 && r.is_ce_itm ? 'ce-itm' : ''}" style="${isR13 ? 'color:#58a6ff;' : ''}">${r.col_4_ce_target}</td>
                    <td class="${!isR13 && r.is_ce_itm ? 'ce-itm' : ''}" style="${isR13 ? 'color:#58a6ff;' : ''}">${r.col_5_ce_greeks}</td>
                    <td class="${!isR13 && r.is_ce_itm ? 'ce-itm' : ''}" style="${isR13 ? 'color:#ff7b72; font-weight:bold;' : ''}">${r.col_6_ce_ltp}</td>
                    
                    <td class="${isR13 ? 'spot-center-box' : ''}" style="font-weight:bold; background:#161b22; color:#58a6ff;">${r.col_7_strike_or_spot}</td>
                    
                    <td class="${!isR13 && r.is_pe_itm ? 'pe-itm' : ''}" style="${isR13 ? 'color:#7ee787; font-weight:bold;' : ''}">${r.col_8_pe_ltp}</td>
                    <td class="${!isR13 && r.is_pe_itm ? 'pe-itm' : ''}" style="${isR13 ? 'color:#7ee787;' : ''}">${r.col_9_pe_greeks}</td>
                    <td class="${!isR13 && r.is_pe_itm ? 'pe-itm' : ''}" style="${isR13 ? 'color:#7ee787;' : ''}">${r.col_10_pe_target}</td>
                    <td class="${!isR13 && r.is_pe_itm ? 'pe-itm' : ''}" style="${isR13 ? 'color:#7ee787;' : ''}">${r.col_11_pe_vol}</td>
                    <td class="${!isR13 && r.is_pe_itm ? 'pe-itm' : ''}" style="${isR13 ? 'color:#d29922;' : ''}">${r.col_12_pe_oichg}</td>
                    <td class="${!isR13 && r.is_pe_itm ? 'pe-itm' : ''}" style="${isR13 ? 'color:#7ee787;' : ''}">${r.col_13_pe_oi}</td>
                </tr>`;
            });

            tbody.innerHTML = html;
        }

        window.onload = () => {
            loadCoaGrid();
            setInterval(loadCoaGrid, 3000);
        };
    </script>
</body>
</html>
