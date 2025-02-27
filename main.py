import asyncio
from machine.machine import Machine
from backend.server import start_backend
from frontend.launcher import start_frontend

async def main():
    """ Orchestrates backend initialization, server startup, and frontend. """
    machine = Machine()

    # Start machine first
    await machine.initialize()

    # Start backend (FastAPI & WebSockets)
    start_backend()

    # Start frontend (PyWebView)
    start_frontend()

if __name__ == "__main__":
    asyncio.run(main())
