import core.logging.queries as Queries
from core.database.database_client import DatabaseClient


class SchemaManager:
    """Manages database schema creation."""
    
    def __init__(self, client: DatabaseClient):
        self.client = client

    async def ensure_tables_exist(self):
        """Ensures required tables exist in the database."""
        await self.client.execute(Queries.CREATE_LOGS_TABLE)
