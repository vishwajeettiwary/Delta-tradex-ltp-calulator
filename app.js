// --- System State & Memory ---
let systemData = {
    previousScenario: "Scenario 1 (Strong - Strong)",
    currentScenario: "Scenario 1 (Strong - Strong)",
    shiftTrackerCall: { state: "Static", time: "09:15 AM" },
    shiftTrackerPut: { state: "Static", time: "09:15 AM" },
    spotPrice: 24114,
    supportStrike: 24000,
    resistanceStrike: 24200
};

// --- Sample Option Chain Data Generator ---
function fetchOptionChainData() {
    let strikes = [23900, 23950, 24000, 24050, 24100, 24150, 24200, 24250, 24300];
    return strikes.map(strike => ({
        strike: strike,
        callOI: Math.floor(Math.random() * 50000) + 10000,
        callLTP: (24200 - strike > 0 ? (24200 - strike) * 0.8 : 25).toFixed(2),
        callState: strike === 24200 ? "Strong" : "Normal",
        putOI: Math.floor(Math.random() * 50000) + 10000,
        putLTP: (strike - 24000 > 0 ? (strike - 24000) * 0.8 : 20).toFixed(2),
        putState: strike === 24000 ? "Strong" : "Normal"
    }));
}

// --- Main Render Function ---
function renderDashboard() {
    const table = document.getElementById("coaTable");
    table.innerHTML = "";

    // 1. Header (Row 1)
    let headerHTML = `
        <tr>
            <th colspan="6">CALL SIDE</th>
            <th>STRIKE</th>
            <th colspan="6">PUT SIDE</th>
        </tr>
        <tr>
            <th>OI</th><th>Vol</th><th>LTP</th><th>EOS/EOR</th><th>State</th><th>Action</th>
            <th>Spot: ${systemData.spotPrice}</th>
            <th>Action</th><th>State</th><th>EOS/EOR</th><th>LTP</th><th>Vol</th><th>OI</th>
        </tr>
    `;
    
    // 2. Row 2: Market State Box (Col 7 Clickable Popup)
    let row2HTML = `
        <tr style="background:#2a2a2a;">
            <td colspan="6">Call Tracker Status</td>
            <td class="clickable bg-green" onclick="showMarketStatePopup()">
                <strong>Market State: BULLISH</strong><br><small>(Click for Details)</small>
            </td>
            <td colspan="6">Put Tracker Status</td>
        </tr>
    `;

    // 3. Middle Rows (Option Chain Data Rows 3 to 11)
    let chainData = fetchOptionChainData();
    let rowsHTML = "";
    chainData.forEach(row => {
        let isSupport = row.strike === systemData.supportStrike;
        let isResistance = row.strike === systemData.resistanceStrike;
        
        rowsHTML += `
            <tr>
                <td>${row.callOI}</td>
                <td>${row.callOI * 2}</td>
                <td class="clickable" onclick="showLTPPopup('CE', ${row.strike}, ${row.callLTP})">${row.callLTP}</td>
                <td>${isResistance ? 'EOR (24218)' : '-'}</td>
                <td class="${isResistance ? 'bg-green' : ''}">${isResistance ? 'STRONG' : ''}</td>
                <td>${isResistance ? 'Safe Sell PE / Sell CE' : '-'}</td>
                
                <td style="font-weight:bold; background:#333;">${row.strike}</td>
                
                <td>${isSupport ? 'Safe Buy CE' : '-'}</td>
                <td class="${isSupport ? 'bg-green' : ''}">${isSupport ? 'STRONG' : ''}</td>
                <td>${isSupport ? 'EOS (23982)' : '-'}</td>
                <td class="clickable" onclick="showLTPPopup('PE', ${row.strike}, ${row.putLTP})">${row.putLTP}</td>
                <td>${row.putOI * 2}</td>
                <td>${row.putOI}</td>
            </tr>
        `;
    });

    // 4. Row 13: Shift Tracker
    let row13HTML = `
        <tr style="background:#1a1a1a;">
            <td colspan="6" class="bg-gray">
                <strong>Call Shift Tracker:</strong> ${systemData.shiftTrackerCall.state} (${systemData.shiftTrackerCall.time})
            </td>
            <td style="background:#000; color:#00bcd4;">ROW 13 LOG</td>
            <td colspan="6" class="bg-gray">
                <strong>Put Shift Tracker:</strong> ${systemData.shiftTrackerPut.state} (${systemData.shiftTrackerPut.time})
            </td>
        </tr>
    `;

    table.innerHTML = headerHTML + row2HTML + rowsHTML + row13HTML;
}

// --- Popup Directives Logic (Rule 5 & Rule 7) ---

function showMarketStatePopup() {
    let body = `
        <h3>🏛️ Market State Scenario Details</h3>
        <hr>
        <p><strong>Previous Scenario:</strong> ${systemData.previousScenario}</p>
        <p><strong>Current Active Scenario:</strong> ${systemData.currentScenario}</p>
        <hr>
        <h4>🎯 Trade Directives (Rule 5):</h4>
        <ul>
            <li><strong>CE Entry:</strong> Safe at EOS (23982) | Risky at EOD (24018)</li>
            <li><strong>PE Entry:</strong> Safe at EOR (24218) | Risky at EOD (24182)</li>
            <li><strong>Reversal Target:</strong> 1 Divergence Prior to Boundaries</li>
        </ul>
    `;
    openModal(body);
}

function showLTPPopup(type, strike, ltp) {
    let entryLevel = type === 'CE' ? 'EOS / EOD' : 'EOR / EOD';
    let slDivergence = type === 'CE' ? strike - 50 : strike + 50;
    
    let body = `
        <h3>📌 ${type} Option Strike Details: ${strike}</h3>
        <hr>
        <p><strong>Current Premium (LTP):</strong> ₹${ltp}</p>
        <p><strong>Recommended Entry Zone:</strong> Entry on ${entryLevel}</p>
        <p><strong>Target Level:</strong> Reversal Divergence</p>
        <p style="color:#ff5252;"><strong>Stop Loss (1 Div Away):</strong> ${slDivergence} Strike Divergence Zone</p>
    `;
    openModal(body);
}

function openModal(content) {
    document.getElementById("modalBody").innerHTML = content;
    document.getElementById("infoModal").style.display = "block";
}

function closeModal() {
    document.getElementById("infoModal").style.display = "none";
}

// Initial Run
window.onload = renderDashboard;
