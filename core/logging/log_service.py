from core.logging.logger_interface import LoggerInterface
from core.logging.database_logger import DatabaseLogger
from core.logging.console_logger import ConsoleLogger

class LogService:
    """Handles logging with a selected logger strategy."""

    logger: LoggerInterface = ConsoleLogger() 
    
    @classmethod
    async def initialize(cls, use_console_logging=False):
        """Initializes logging and allows switching between database and console logging."""
        if use_console_logging: 
            cls.logger = ConsoleLogger()
        else:
            cls.logger = DatabaseLogger()

        # Initialize database if using DatabaseLogger
        if isinstance(cls.logger, DatabaseLogger):
            await cls.logger.initialize_database()

    @classmethod
    def log(cls, text, log_level="INFO"):
        """Logs a message synchronously."""
        cls.logger.log(log_level, text)

    @classmethod
    async def log_async(cls, text, log_level="INFO"):
        """Logs a message asynchronously."""
        await cls.logger.log_async(log_level, text)
