from core.database.database_client import DatabaseClient
import machine.db.queries as Queries

class MachineRepository:
    """Handles database operations related to machine events."""

    def __init__(self, db_client: DatabaseClient, db_path="app.db"):
        self.client: DatabaseClient = db_client
        self.db_path = db_path

    async def initialize_database(self):
        """Ensures the machine events table exists."""
        await self.client.connect(self.db_path)
        await self.client.execute(Queries.CREATE_MACHINE_EVENTS_TABLE)
        await self.client.execute(Queries.CREATE_TIMESTAMP_INDEX)

    async def log_event(self, event_type: str, event_details: str, severity: str = "INFO"):
        """Logs a machine event."""
        await self.client.execute(
            Queries.INSERT_MACHINE_EVENT,
            (event_type, event_details, severity)
        )

    async def get_all_events(self):
        """Fetches all machine events."""
        return await self.client.fetch_all(Queries.FETCH_MACHINE_EVENTS)

    async def clear_events(self):
        """Deletes all machine events."""
        await self.client.execute(Queries.CLEAR_MACHINE_EVENTS)

    async def close(self):
        """Closes the database connection."""
        await self.client.close()
