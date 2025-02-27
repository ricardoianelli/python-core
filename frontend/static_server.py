from fastapi.staticfiles import StaticFiles
import os

def configure_static_files(app):
    """ Serves static frontend files. """
    WEB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "web"))
    app.mount("/", StaticFiles(directory=WEB_DIR, html=True), name="static")
