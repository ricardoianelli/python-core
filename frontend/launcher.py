import webview

def start_frontend():
    """ Starts the PyWebView frontend. """
    webview.create_window("My App", "http://127.0.0.1:8000")
    webview.start()
