import logging
from core.logging.database_service import LoggingDatabaseService
from database.clients.sqlite_client import SQLiteClient

class Logger:
    def __init__(self):
        self.db_service = LoggingDatabaseService(SQLiteClient())
        
    async def initialize(self):
        """Ensure the logging database is initialized before use."""
        await self.db_service.initialize_database()

    async def log(self, level: str, message: str):
        """Logs a message asynchronously in the database and console."""
        await self.db_service.log(level, message)
        logging.info(f"[{level}] {message}")
