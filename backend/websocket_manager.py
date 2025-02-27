from fastapi import WebSocket
import json

class WebSocketManager:
    """ Manages all WebSocket connections and message handling. """
    
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        """ Accepts a new WebSocket connection. """
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"🔗 WebSocket connected: {websocket.client}")

    async def disconnect(self, websocket: WebSocket):
        """ Removes a WebSocket connection. """
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print(f"❌ WebSocket disconnected: {websocket.client}")

    async def broadcast(self, message: dict):
        """ Sends a message to all connected clients. """
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))

    async def handle_message(self, websocket: WebSocket):
        """ Listens for incoming messages. """
        try:
            while True:
                data = await websocket.receive_text()
                print(f"📩 Received from frontend: {data}")
                response = {"response": f"Server received: {data}"}
                await self.broadcast(response)
        except Exception as e:
            print(f"⚠️ WebSocket error: {e}")
        finally:
            await self.disconnect(websocket)
