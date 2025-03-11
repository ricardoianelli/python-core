from fastapi import WebSocket
import json
from typing import Callable, Dict, List

class WebSocketManager:
    """Manages WebSocket connections and allows static subscriptions to incoming messages."""

    active_connections: List[WebSocket] = []
    _incoming_subscribers: Dict[str, List[Callable]] = {}

    @classmethod
    async def connect(cls, websocket: WebSocket):
        """Accepts a new WebSocket connection."""
        await websocket.accept()
        cls.active_connections.append(websocket)
        print(f"🔗 WebSocket connected: {websocket.client}")

    @classmethod
    async def disconnect(cls, websocket: WebSocket):
        """Removes a WebSocket connection."""
        if websocket in cls.active_connections:
            cls.active_connections.remove(websocket)
            print(f"❌ WebSocket disconnected: {websocket.client}")

    @classmethod
    async def broadcast(cls, message: dict):
        """Sends a message to all connected clients, with error handling."""
        disconnected_clients = []
        for connection in cls.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                print(f"⚠️ WebSocket send failed: {e}")
                disconnected_clients.append(connection)

        # Remove disconnected clients
        for client in disconnected_clients:
            await cls.disconnect(client)


    @classmethod
    def subscribe_to_incoming(cls, message_type: str, callback: Callable):
        """Allows any part of the system to subscribe to incoming WebSocket messages."""
        if message_type not in cls._incoming_subscribers:
            cls._incoming_subscribers[message_type] = []
        cls._incoming_subscribers[message_type].append(callback)

    @classmethod
    async def handle_message(cls, websocket: WebSocket):
        """Listens for incoming messages and dispatches them to subscribers."""
        try:
            while True:
                data = await websocket.receive_text()
                print(f"📩 Received from frontend: {data}")
                message = json.loads(data)
                message_type = message.get("type")

                # Notify all subscribers of this message type
                if message_type in cls._incoming_subscribers:
                    for callback in cls._incoming_subscribers[message_type]:
                        await callback(message)

        except Exception as e:
            print(f"⚠️ WebSocket error: {e}")
        finally:
            await cls.disconnect(websocket)
