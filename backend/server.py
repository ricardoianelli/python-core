import webview
import os
from backend.api import AppAPI

def start_server():
    """Configures and launches the PyWebView application."""
    static_dir = os.path.abspath("web")

    api = AppAPI()  # Instantiate API

    webview.create_window(
        title="My App",
        url=f"{static_dir}/index.html",
        js_api=api,
    )
    
    webview.start(debug=True)
