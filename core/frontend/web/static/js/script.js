let socket;

function connectWebSocket() {
    socket = new WebSocket("ws://127.0.0.1:8000/ws");

    socket.onopen = function() {
        console.log("WebSocket connected!");
        socket.send("Hello Server!");
    };

    socket.onmessage = function(event) {
        let message = JSON.parse(event.data);
        document.getElementById("response").innerText = message.response;
    };

    socket.onerror = function(error) {
        console.log("WebSocket Error:", error);
    };

    socket.onclose = function() {
        console.log("WebSocket Disconnected");
    };
}

function sendMessage() {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send("Hello from frontend!");
    } else {
        console.log("WebSocket not connected.");
    }
}


connectWebSocket();