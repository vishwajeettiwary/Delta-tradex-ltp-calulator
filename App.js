// =========================================================================
// SYSTEM STATE & MASTER DATA MODEL (Integrated Phase 1 Rules 1 to 8)
// =========================================================================
const systemState = {
    spotPrice: 24114,
    supportStrike: 24000,
    resistanceStrike: 24200,
    activeEOS: 23982,
    activeEOR: 24218,
    previousScenario: "Scenario 1: Support Strong + Resistance Strong",
    currentScenarioId: 3, // Rule 5: Scenario 3
    scenarios: {
        1: { name: "Support Strong + Resistance Strong", state: "Consolidating / Range-Bound", ceAction: "Safe Buy @ EOS (23982) | Risky @ EOD", peAction: "Safe Buy @ EOR (24218) | Risky @ EOD", exit: "Reversal at Opposing Boundary" },
        2: { name: "Support Strong + Resistance WTB", state: "Bearish Bias (Top Pressure)", ceAction: "AVOID CALL BUYING 🚫", peAction: "Safe Buy @ EOR | Aggressive @ Top Div", exit: "Next Support Divergence" },
        3: { name: "Support Strong + Resistance WTT", state: "Bullish Bias (Upward Target)", ceAction: "Safe Buy @ EOS (23982) | Risky @ EOD", peAction: "AVOID PUT BUYING 🚫", exit: "1 Divergence Prior to Target WTT Strike" },
        4: { name: "Support WTB + Resistance Strong", state: "Bearish Bias (Downward Fall)", ceAction: "AVOID CALL BUYING 🚫", peAction: "Safe Buy @ EOR | Risky @ EOD", exit: "1 Divergence Below Support" },
        5: { name: "Support WTT + Resistance Strong", state: "Bullish Bias (Support Creeping UP)", ceAction: "Safe Buy @ EOS | Risky @ EOD", peAction: "AVOID PUT BUYING 🚫", exit: "1 Divergence Above Resistance" },
        6: { name: "Support WTB + Resistance WTB", state: "🩸 Severe Bearish (Blood Bath)", ceAction: "STRICTLY BANNED 🚫", peAction: "Safe Buy @ EOR / Aggressive @ EOD", exit: "Trailing SL Only" },
        7: { name: "Support WTT + Resistance WTT", state: "🚀 Severe Bullish (Bull Run)", ceAction: "Safe Buy @ EOS / Aggressive @ EOD", peAction: "STRICTLY BANNED 🚫", exit: "Trailing SL Only" },
        8: { name: "Support WTT + Resistance WTB", state: "Neutral / Conflicting (COA 2.0)", ceAction: "Wait for OI Confirmation", peAction: "Wait for OI Confirmation", exit: "Scalp Only" },
        9: { name: "Support WTB + Resistance WTT", state: "Neutral / Conflicting (COA 2.0)", ceAction: "Wait for Speed Analysis", peAction: "Wait for Speed Analysis", exit: "Scalp Only" }
    },
    // Rule 4: 60-Minute Absorption Tracker Memory
    shiftLogCall: { state: "Weak Towards Top (WTT to 24250)", startTime: "09:45 AM", timerMinutes: 42, status: "Absorbing (Unconfirmed)" },
    shiftLogPut: { state: "Static / Solidified", startTime: "09:15 AM", timerMinutes: 60, status: "Confirmed Strong" }
};

// Option Chain Strikes Array
const strikesData = [
    { strike: 24300, ceOI: 65000, ceVol: 120000, ceLTP: 18.20, ceState: "Normal", peOI: 5000, peVol: 12000, peLTP: 195.40, peState: "Normal" },
    { strike: 24250, ceOI: 82000, ceVol: 190000, ceLTP: 32.50, ceState: "WTT Zone", peOI: 12000, peVol: 25000, peLTP: 158.10, peState: "Normal" },
    { strike: 24200, ceOI: 110000, ceVol: 280000, ceLTP: 54.00, ceState: "STRONG RES", peOI: 25000, peVol: 60000, peLTP: 128.50, peState: "Normal" },
    { strike: 24150, ceOI: 45000, ceVol: 110000, ceLTP: 82.10, ceState: "Normal", peOI: 42000, peVol: 95000, peLTP: 102.30, peState: "Normal" },
    { strike: 24100, ceOI: 30000, ceVol: 85000, ceLTP: 115.40, ceState: "Normal", peOI: 55000, peVol: 130000, peLTP: 81.00, peState: "Normal" },
    { strike: 24050, ceOI: 18000, ceVol: 45000, ceLTP: 152.00, ceState: "Normal", peOI: 78000, peVol: 175000, peLTP: 62.50, peState: "Normal" },
    { strike: 24000, ceOI: 12000, ceVol: 30000, ceLTP: 192.50, ceState: "Normal", peOI: 135000, peVol: 310000, peLTP: 45.20, peState: "STRONG SUP" },
    { strike: 23950, ceOI: 5000, ceVol: 10000, ceLTP: 238.00, ceState: "Normal", peOI: 62000, peVol: 140000, peLTP: 31.10, peState: "Normal" },
    { strike: 23900, ceOI: 2000, ceVol: 4000, ceLTP: 285.00, ceState: "Normal", peOI: 41000, peVol: 90000, peLTP: 21.00, peState: "Normal" }
];

// =========================================================================
// RENDER ENGINE FOR TABLE & OUTER PANELS
// =========================================================================
function renderMasterDashboard() {
    const table = document.getElementById("coaMasterTable");
    table.innerHTML = "";

    // 1. Header (13 Columns Matrix)
    let headerHTML = `
        <thead>
            <tr>
                <th colspan="6">CALL SIDE (RESISTANCE ANALYSIS)</th>
                <th style="background:#00838f; color:#fff;">STRIKE</th>
                <th colspan="6">PUT SIDE (SUPPORT ANALYSIS)</th>
            </tr>
            <tr>
                <th>OI</th><th>Volume</th><th>LTP</th><th>EOS/EOR/Div</th><th>State</th><th>Action</th>
                <th style="background:#222; color:var(--accent-cyan)">SPOT: ${systemState.spotPrice}</th>
                <th>Action</th><th>State</th><th>EOS/EOR/Div</th><th>LTP</th><th>Volume</th><th>OI</th>
            </tr>
        </thead>
    `;

    // 2. Row 2: Col 7 Market State Popup Launcher (Rule 5)
    const activeScen = systemState.scenarios[systemState.currentScenarioId];
    let row2HTML = `
        <tr style="background:#1f1f1f;">
            <td colspan="6" style="color:#aaa;">Call Tracking Zone</td>
            <td class="clickable" onclick="openMarketStateModal()" style="padding:8px; background:#00695c; font-weight:bold;">
                📌 MARKET STATE: ${activeScen.state.toUpperCase()}<br>
                <small style="font-weight:normal; text-decoration:underline;">(Rule 5 Active Pop-up)</small>
            </td>
            <td colspan="6" style="color:#aaa;">Put Tracking Zone</td>
        </tr>
    `;

    // 3. Middle Rows (Option Chain Data Rows 3 to 11)
    let bodyHTML = "<tbody>" + row2HTML;

    strikesData.forEach(row => {
        const isITMCall = row.strike < systemState.spotPrice;
        const isITMPut = row.strike > systemState.spotPrice;
        const isSupport = row.strike === systemState.supportStrike;
        const isResistance = row.strike === systemState.resistanceStrike;

        // Rule 6 Inter-Strike Dynamic Calculation
        let callDivValue = isResistance ? `EOR (${systemState.activeEOR})` : `Div (${row.strike + 18})`;
        let putDivValue = isSupport ? `EOS (${systemState.activeEOS})` : `Div (${row.strike - 18})`;

        let callStateClass = isResistance ? 'bg-strong' : (row.strike === 24250 ? 'bg-wtt' : '');
        let putStateClass = isSupport ? 'bg-strong' : '';

        bodyHTML += `
            <tr>
                <td class="${isITMCall ? 'bg-itm' : ''}">${row.ceOI.toLocaleString()}</td>
                <td class="${isITMCall ? 'bg-itm' : ''}">${row.ceVol.toLocaleString()}</td>
                <td class="${isITMCall ? 'bg-itm' : ''} clickable" onclick="openLTPModal('CALL', ${row.strike}, ${row.ceLTP})">
                    <strong>₹${row.ceLTP.toFixed(2)}</strong>
                </td>
                <td class="${isITMCall ? 'bg-itm' : ''}">${callDivValue}</td>
                <td class="${callStateClass}">${row.ceState}</td>
                <td class="${isITMCall ? 'bg-itm' : ''}">${isResistance ? 'Safe Sell Zone' : '-'}</td>

                <td style="font-weight:bold; background:#282828; color:var(--accent-cyan);">${row.strike}</td>

                <td class="${isITMPut ? 'bg-itm' : ''}">${isSupport ? 'Safe CE Buy Zone' : '-'}</td>
                <td class="${putStateClass}">${row.peState}</td>
                <td class="${isITMPut ? 'bg-itm' : ''}">${putDivValue}</td>
                <td class="${isITMPut ? 'bg-itm' : ''} clickable" onclick="openLTPModal('PUT', ${row.strike}, ${row.peLTP})">
                    <strong>₹${row.peLTP.toFixed(2)}</strong>
                </td>
                <td class="${isITMPut ? 'bg-itm' : ''}">${row.peVol.toLocaleString()}</td>
                <td class="${isITMPut ? 'bg-itm' : ''}">${row.peOI.toLocaleString()}</td>
            </tr>
        `;
    });

    // 4. Row 13 Log Tracker (Rule 4)
    let row13HTML = `
        <tr class="shift-tracker-row">
            <td colspan="6" style="border-right: 2px solid var(--accent-cyan);">
                📊 <strong>CALL SHIFT TRACKER (Rule 4):</strong> 
                <span style="color:var(--yellow-wt);">${systemState.shiftLogCall.state}</span> | 
                Timer: <strong>${systemState.shiftLogCall.timerMinutes} Mins</strong> (${systemState.shiftLogCall.status})
            </td>
            <td style="background:#000; color:var(--accent-cyan);">ROW 13 LOG</td>
            <td colspan="6">
                📊 <strong>PUT SHIFT TRACKER (Rule 4):</strong> 
                <span style="color:#81c784;">${systemState.shiftLogPut.state}</span> | 
                Timer: <strong>${systemState.shiftLogPut.timerMinutes} Mins</strong> (${systemState.shiftLogPut.status})
            </td>
        </tr>
    </tbody>`;

    table.innerHTML = headerHTML + bodyHTML + row13HTML;
}

// Modal Trigger Logics (Rule 5 & 7)
function openMarketStateModal() {
    const scen = systemState.scenarios[systemState.currentScenarioId];
    document.getElementById("modalTitle").innerText = `🏛️ Rule 5: COA Scenario Analysis`;
    
    let content = `
        <div class="directive-badge">
            <strong>Previous Market State:</strong> ${systemState.previousScenario}
        </div>
        <div class="directive-badge" style="border-left-color: var(--yellow-wt);">
            <strong>Current Active Scenario:</strong> Scenario ${systemState.currentScenarioId} - ${scen.name}
        </div>
        <hr style="border-color:var(--border-color); margin: 10px 0;">
        <h4 style="color:var(--accent-cyan);">🎯 Dynamic Execution Directives:</h4>
        <p style="margin-top:6px;">• <strong>Call (CE) Action:</strong> ${scen.ceAction}</p>
        <p style="margin-top:4px;">• <strong>Put (PE) Action:</strong> ${scen.peAction}</p>
        <p style="margin-top:4px;">• <strong>Target Exit Point:</strong> ${scen.exit}</p>
        <hr style="border-color:var(--border-color); margin: 10px 0;">
        <p style="font-size:11px; color:#aaa;">
            <strong>Calculated Day Range (Rule 6):</strong> Active EOS [${systemState.activeEOS}] to Active EOR [${systemState.activeEOR}]
        </p>
    `;
    
    document.getElementById("modalContent").innerHTML = content;
    document.getElementById("masterModal").style.display = "flex";
}

function openLTPModal(type, strike, ltp) {
    document.getElementById("modalTitle").innerText = `📌 ${type} Option Details - Strike ${strike}`;
    
    let isCE = type === 'CALL';
    let targetDivergence = isCE ? strike - 18 : strike + 18;
    let stopLossLevel = isCE ? strike - 68 : strike + 68; // Rule 7: 1 Divergence Below/Away

    let content = `
        <p><strong>Current Option Premium (LTP):</strong> <span style="font-size:16px; color:var(--accent-cyan);">₹${ltp.toFixed(2)}</span></p>
        <div class="directive-badge" style="margin-top:10px;">
            <strong>Entry Directive:</strong> ${isCE ? 'Safe Entry @ EOS / EOD' : 'Safe Entry @ EOR / EOD'}
        </div>
        <p style="margin-top:8px;">• <strong>Target Index Level:</strong> ${targetDivergence} Divergence Zone</p>
        
        <div class="sl-alert">
            🛑 <strong>Rule 7 Stop Loss Theorem:</strong><br>
            Set SL exactly 1 Divergence away at <strong>${stopLossLevel} Zone</strong>. Do not hold if the price breaks this level.
        </div>
    `;

    document.getElementById("modalContent").innerHTML = content;
    document.getElementById("masterModal").style.display = "flex";
}

function closeModal() {
    document.getElementById("masterModal").style.display = "none";
}

// Window Load Engine Trigger
window.onload = renderMasterDashboard;
