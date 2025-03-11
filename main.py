import asyncio
from core.logging.log_service import LogService
from machine.machine import Machine
from core.backend.server import start_backend
from core.frontend.launcher import start_frontend


async def main():
    """ Orchestrates backend initialization, server startup, and frontend. """

    await LogService.initialize(use_console_logging=False)
    
    await LogService.log_async("Initializing Python Core...")
    
    machine = Machine()

    # Start machine first
    await machine.initialize()

    # Start backend (FastAPI & WebSockets)
    start_backend()

    # Start frontend (PyWebView)
    start_frontend()
    
    await LogService.log_async("Python Core Initialized!")

if __name__ == "__main__":
    asyncio.run(main())
