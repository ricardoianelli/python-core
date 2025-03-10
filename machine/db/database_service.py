import machine.db.queries as Queries
from database.database_client import DatabaseClient

class MachineDatabaseService:
    """Handles database operations for machine events."""

    def __init__(self, client: DatabaseClient):
        self.client = client

    async def initialize_database(self) -> None:
        """Ensure machine events table exists asynchronously."""
        await self.client.connect()
        await self.client.execute(Queries.CREATE_MACHINE_EVENTS_TABLE)

    async def insert_event(self, event_type: str, details: str) -> None:
        """Insert a machine event asynchronously."""
        await self.client.execute(Queries.INSERT_MACHINE_EVENT, (event_type, details))

    async def fetch_events(self):
        """Fetch all machine events."""
        return await self.client.fetch_all(Queries.FETCH_MACHINE_EVENTS)

    async def close(self) -> None:
        """Close the database connection asynchronously."""
        await self.client.close()
