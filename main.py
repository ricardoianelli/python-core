import asyncio
from backend.machine import Machine
from backend.server import start_server
from backend.frontend import start_frontend

async def main():
    """ Orchestrates backend initialization, Uvicorn, and PyWebView. """
    machine = Machine()

    # Start backend initialization
    await machine.initialize()

    # Start Uvicorn (API & WebSockets)
    start_server()

    # Start frontend (PyWebView)
    start_frontend()

if __name__ == "__main__":
    asyncio.run(main())
