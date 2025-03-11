let socket;

function connectWebSocket() {
    socket = new WebSocket("ws://127.0.0.1:8000/ws");

    socket.onopen = function () {
        console.log("WebSocket connected!");
        socket.send(JSON.stringify({ type: "fetch_logs" }));
    };

    socket.onmessage = function (event) {
        let message = JSON.parse(event.data);
        
        if (message.type === "all_logs") {
            displayLogs(message.logs);
        } else if (message.type === "new_log") {
            appendLog(message);
        }
    };

    socket.onerror = function (error) {
        console.log("WebSocket Error:", error);
    };

    socket.onclose = function () {
        console.log("WebSocket Disconnected");
    };
}

// Send log to backend
function sendLog() {
    let logMessage = document.getElementById("logMessage").value;
    let logLevel = document.getElementById("logLevel").value;

    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ type: "add_log", log_level: logLevel, message: logMessage }));
        document.getElementById("logMessage").value = ""; // Clear input after sending
    } else {
        console.log("WebSocket not connected.");
    }
}

// Display logs in the UI
function displayLogs(logs) {
    let logContainer = document.getElementById("logContainer");
    logContainer.innerHTML = ""; // Clear previous logs

    logs.forEach(log => {
        appendLog(log);
    });
}

// Append a single log entry to the UI
function appendLog(log) {
    let logContainer = document.getElementById("logContainer");
    let logElement = document.createElement("div");
    logElement.textContent = `[${log.timestamp}] ${log.log_level}: ${log.message}`;
    logContainer.appendChild(logElement);
}

connectWebSocket();
