from fastapi import FastAPI, WebSocket
from core.backend.websocket_manager import WebSocketManager
from core.logging.log_service import LogService

app = FastAPI()

LogService()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """ WebSocket connection endpoint. """
    await WebSocketManager.connect(websocket)
    await WebSocketManager.handle_message(websocket)
