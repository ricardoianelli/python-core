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
        } else if (message.type === "log_deleted") {
            removeLogFromUI(message.id);
        } else if (message.type === "logs_cleared") {
            clearLogsFromUI();
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

// Send request to clear logs
function clearLogs() {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ type: "clear_logs" }));
    }
}

// Send request to delete a single log
function deleteLog(id) {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ type: "delete_log", id: id }));
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
    logElement.classList.add("log-entry");
    logElement.setAttribute("id", `log-${log.id}`);

    logElement.innerHTML = `
        <span>[${log.timestamp}] ${log.log_level}: ${log.message}</span>
        <button class="delete-btn" onclick="deleteLog(${log.id})">Delete</button>
    `;

    logContainer.appendChild(logElement);
}

// Remove a single log entry from the UI
function removeLogFromUI(id) {
    let logElement = document.getElementById(`log-${id}`);
    if (logElement) {
        logElement.remove();
    }
}

// Clear all logs from the UI
function clearLogsFromUI() {
    document.getElementById("logContainer").innerHTML = "";
}

connectWebSocket();
