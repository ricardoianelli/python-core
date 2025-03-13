from core.database.database_client import DatabaseClient
import core.logging.queries as Queries

class LogRepository:
    """Handles all database operations for logs."""

    def __init__(self, db_client: DatabaseClient, db_path="app.db"):
        self.client: DatabaseClient = db_client
        self.db_path = db_path

    async def initialize_database(self):
        """Ensures the logs table exists."""
        await self.client.connect(self.db_path)
        await self.client.execute(Queries.CREATE_LOGS_TABLE)
        await self.client.execute(Queries.CREATE_TIMESTAMP_INDEX)
        
    async def add_log(self, log_level: str, message: str, timestamp: str):
        """Inserts a log into the database using the provided timestamp."""
        await self.client.execute(Queries.INSERT_LOG, (log_level, message, timestamp))

    async def get_logs(self):
        """Fetches all logs from the database."""
        return await self.client.fetch_all(Queries.FETCH_ALL_LOGS)

    async def get_logs_by_level(self, log_level: str):
        """Fetches logs filtered by log level."""
        return await self.client.fetch_all(Queries.FETCH_LOGS_BY_LEVEL, (log_level,))

    async def delete_old_logs(self, max_entries: int):
        """Deletes logs older than the latest 'max_entries' records."""
        await self.client.execute(Queries.DELETE_OLD_LOGS, (max_entries,))

    async def delete_log(self, log_id: int):
        """Deletes a log by ID."""
        await self.client.execute(Queries.DELETE_LOG_BY_ID, (log_id,))

    async def clear_logs(self):
        """Deletes all logs."""
        await self.client.execute(Queries.CLEAR_ALL_LOGS)

    async def close(self):
        """Closes the database connection."""
        await self.client.close()
