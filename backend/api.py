from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
import os
from backend.websocket_manager import WebSocketManager

app = FastAPI()

ws_manager = WebSocketManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """ WebSocket connection endpoint. """
    await ws_manager.connect(websocket)
    await ws_manager.handle_message(websocket)

# Get absolute path of the web directory
WEB_DIR = os.path.abspath("web")

# Serve static files (HTML, CSS, JS)
app.mount("/", StaticFiles(directory=WEB_DIR, html=True), name="static")