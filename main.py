import asyncio
from machine.machine import Machine
from core.backend.server import start_backend
from core.frontend.launcher import start_frontend
from core.logging.logger import Logger

async def main():
    """ Orchestrates backend initialization, server startup, and frontend. """
    
    logger = Logger()
    await logger.initialize()
    
    await logger.log("INFO", "Initializing system...")

    machine = Machine()

    # Start machine first
    await machine.initialize()
    await logger.log("INFO", "Machine initialized successfully.")

    # Start backend (FastAPI & WebSockets)
    start_backend()
    await logger.log("INFO", "Backend started.")

    # Start frontend (PyWebView)
    start_frontend()
    await logger.log("INFO", "Frontend started.")

    await logger.log("INFO", "System successfully initialized.")

if __name__ == "__main__":
    asyncio.run(main())
