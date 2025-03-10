import threading
import asyncio
import uvicorn
from core.backend.api import app
from core.frontend.static_server import configure_static_files  # Moved to frontend

def start_uvicorn():
    """ Runs Uvicorn in a separate thread using a proper event loop. """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Configure static file serving (now in frontend)
    configure_static_files(app)

    # Configure and start Uvicorn server
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)

    # Run the server inside an event loop
    loop.run_until_complete(server.serve())

def start_backend():
    """ Starts the FastAPI Web Server in a new thread. """
    server_thread = threading.Thread(target=start_uvicorn, daemon=True)
    server_thread.start()
