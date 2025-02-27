import threading
import webview
import uvicorn
from backend.api import app

def start_uvicorn():
    """ Runs Uvicorn in a separate thread. """
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

def start_app():
    """ Starts Uvicorn and PyWebView. """
    server_thread = threading.Thread(target=start_uvicorn, daemon=True)
    server_thread.start()

    # Start PyWebView pointing to the locally running WebSocket server
    webview.create_window("My App", "http://127.0.0.1:8000")
    webview.start(debug=True)

if __name__ == "__main__":
    start_app()
