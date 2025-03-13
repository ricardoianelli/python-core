from core.logging.logger_interface import LoggerInterface
from core.logging.console_logger import ConsoleLogger
from core.logging.database_logger import DatabaseLogger

class LogService:
    """Handles logging through configured loggers."""

    logger: LoggerInterface = ConsoleLogger()  # Default to console logging

    @classmethod
    async def initialize(cls, log_to_database=False):
        """Initializes logging with the chosen logger."""
        cls.logger = DatabaseLogger() if log_to_database else ConsoleLogger()
        await cls.logger.initialize()  # Ensure DB schema is created if needed

    @classmethod
    async def log_async(cls, text, log_level="INFO"):
        """Logs an async message."""
        await cls.logger.log_async(text, log_level)

    @classmethod
    def log(cls, text, log_level="INFO"):
        """Logs a sync message."""
        cls.logger.log(text, log_level)
