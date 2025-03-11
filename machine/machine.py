import asyncio

from core.logging.log_service import LogService

class Machine:
    """ Manages the lifecycle of the machine. """

    def __init__(self):
        self.running = False

    async def on_starting(self):
        """ Called before the machine starts. """
        await LogService.log_async("🚀 Machine is starting...")

    async def on_started(self):
        """ Called when the machine is fully started. """
        self.running = True
        await LogService.log_async("✅ Machine started successfully!")

    async def on_shutting_down(self):
        """ Called before the machine shuts down. """
        await LogService.log_async("⚠️ Machine is shutting down...")

    async def on_shutdown(self):
        """ Called when the machine is completely shut down. """
        self.running = False
        await LogService.log_async("🔴 Machine has shut down.")

    async def initialize(self):
        """ Runs the full machine startup sequence asynchronously. """
        await self.on_starting()
        
        await asyncio.sleep(1)  # Simulate startup delay
        
        await self.on_started()

    async def shutdown(self):
        """ Runs the shutdown sequence asynchronously. """
        await self.on_shutting_down()
        
        await asyncio.sleep(1)  # Simulate shutdown delay
        
        await self.on_shutdown()
