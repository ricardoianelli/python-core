import aiosqlite
from core.logging import queries

class LogRepository:
    """Handles all database operations for logs."""

    def __init__(self, db_path="app.db"):
        self.db_path = db_path

    async def initialize_database(self):
        """Ensures the logs table exists."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(queries.CREATE_LOGS_TABLE)
            await db.commit()

    async def add_log(self, log_level: str, message: str, timestamp: str):
        """Inserts a log into the database using the provided timestamp."""
        async with aiosqlite.connect("app.db") as db:
            await db.execute(queries.INSERT_LOG, (log_level, message, timestamp))
            await db.commit()

    async def get_logs(self):
        """Fetches all logs from the database."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(queries.FETCH_ALL_LOGS) as cursor:
                rows = await cursor.fetchall()
                return [{"id": row[0], "log_level": row[1], "message": row[2], "timestamp": row[3]} for row in rows]

    async def get_logs_by_level(self, log_level: str):
        """Fetches logs filtered by log level."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(queries.FETCH_LOGS_BY_LEVEL, (log_level,)) as cursor:
                rows = await cursor.fetchall()
                return [{"id": row[0], "log_level": row[1], "message": row[2], "timestamp": row[3]} for row in rows]

    async def delete_old_logs(self, max_entries: int):
        """Deletes logs older than the latest 'max_entries' records."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(queries.DELETE_OLD_LOGS, (max_entries,))
            await db.commit()
            
    async def delete_log(self, log_id: int):
        """Deletes a log by ID."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(queries.DELETE_LOG_BY_ID, (log_id,))
            await db.commit()

    async def clear_logs(self):
        """Deletes all logs."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(queries.CLEAR_ALL_LOGS)
            await db.commit()
