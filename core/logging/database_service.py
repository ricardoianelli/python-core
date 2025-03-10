import logging
import core.logging.queries as Queries
from database.database_client import DatabaseClient

class LoggingDatabaseService:
    """Handles database operations for logging."""

    def __init__(self, client: DatabaseClient):
        self.client = client

    async def initialize_database(self) -> None:
        """Ensure log tables exist asynchronously."""
        await self.client.connect()
        await self.client.execute(Queries.CREATE_LOGS_TABLE)
        logging.info("✅ Logging database initialized.")

    async def log(self, log_level: str, message: str) -> None:
        """Logs a message asynchronously in the database."""
        await self.client.execute(Queries.INSERT_LOG, (log_level, message))
        logging.info(f"[{log_level}] {message}")

    async def fetch_logs(self):
        """Fetch all logs."""
        return await self.client.fetch_all(Queries.FETCH_ALL_LOGS)

    async def close(self) -> None:
        """Close the database connection asynchronously."""
        await self.client.close()
