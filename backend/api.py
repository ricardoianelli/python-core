from fastapi import FastAPI, WebSocket
from backend.websocket_manager import WebSocketManager

app = FastAPI()
ws_manager = WebSocketManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """ WebSocket connection endpoint. """
    await ws_manager.connect(websocket)
    await ws_manager.handle_message(websocket)
