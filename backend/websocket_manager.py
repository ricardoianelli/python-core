from fastapi import WebSocket
import json

class WebSocketManager:
    """ Manages all WebSocket connections and message handling. """
    
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        """ Accepts a new WebSocket connection and adds it to the list. """
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"New WebSocket Connection: {websocket.client}")

    async def disconnect(self, websocket: WebSocket):
        """ Removes a WebSocket connection when it closes. """
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print(f"WebSocket Disconnected: {websocket.client}")

    async def broadcast(self, message: dict):
        """ Sends a message to all connected clients. """
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))

    async def handle_message(self, websocket: WebSocket):
        """ Listens for incoming messages and processes them. """
        try:
            while True:
                data = await websocket.receive_text()
                print(f"Received from frontend: {data}")

                # Example: Send a response back to all clients
                response = {"response": f"Server received: {data}"}
                await self.broadcast(response)
        
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await self.disconnect(websocket)
