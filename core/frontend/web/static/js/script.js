let socket;
let allLogs = [];  // Store logs in memory for filtering

function connectWebSocket() {
    socket = new WebSocket("ws://127.0.0.1:8000/ws");

    socket.onopen = function () {
        console.log("WebSocket connected!");
        socket.send(JSON.stringify({ type: "fetch_logs" }));
    };

    socket.onmessage = function (event) {
        let message = JSON.parse(event.data);
        
        if (message.type === "all_logs") {
            allLogs = message.logs;
            filterLogs(); // Display logs based on the current filter
        } else if (message.type === "new_log") {
            allLogs.push(message);
            filterLogs();
        } else if (message.type === "log_deleted") {
            allLogs = allLogs.filter(log => log.id !== message.id);
            filterLogs();
        } else if (message.type === "logs_cleared") {
            allLogs = [];
            filterLogs();
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

// Display logs based on the selected filter
function filterLogs() {
    let filterLevel = document.getElementById("filterLevel").value;
    let filteredLogs = filterLevel === "ALL" ? allLogs : allLogs.filter(log => log.log_level === filterLevel);
    
    let logContainer = document.getElementById("logContainer");
    logContainer.innerHTML = ""; // Clear previous logs

    filteredLogs.forEach(log => {
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

connectWebSocket();
