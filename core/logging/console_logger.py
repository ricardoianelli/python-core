import asyncio
from datetime import datetime
from core.logging.logger_interface import LoggerInterface

class ConsoleLogger(LoggerInterface):
    """Logs messages to the console (stdout)."""

    async def log_async(self, log_level: str, message: str):
        """Logs a message asynchronously to the console."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {log_level}: {message}")

    def log(self, log_level: str, message: str):
        """Logs a message synchronously to the console."""
        asyncio.run(self.log_async(log_level, message))
