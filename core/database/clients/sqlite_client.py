import aiosqlite
from typing import Any, List, Dict, Optional
from database.database_client import DatabaseClient

class SQLiteClient(DatabaseClient):
    def __init__(self):
        self.connection: Optional[aiosqlite.Connection] = None
        self.db_path: str = "app.db"

    async def connect(self, db_path: str = "app.db") -> None:
        """Establish an async connection to the database."""
        self.db_path = db_path
        if self.connection is None:
            self.connection = await aiosqlite.connect(self.db_path)

    async def execute(self, query: str, params: tuple = ()) -> None:
        """Execute a query asynchronously (INSERT, UPDATE, DELETE)."""
        if not self.connection:  # Ensure connection is established
            raise RuntimeError("Database connection is not established. Call `connect()` first.")

        async with self.connection.execute(query, params):
            await self.connection.commit()

    async def fetch_one(self, query: str, params: tuple = ()) -> Any:
        """Fetch a single record asynchronously."""
        if not self.connection:
            raise RuntimeError("Database connection is not established. Call `connect()` first.")

        async with self.connection.execute(query, params) as cursor:
            return await cursor.fetchone()

    async def fetch_all(self, query: str, params: tuple = ()) -> List[Dict]:
        """Fetch multiple records asynchronously."""
        if not self.connection:
            raise RuntimeError("Database connection is not established. Call `connect()` first.")

        async with self.connection.execute(query, params) as cursor:
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in await cursor.fetchall()]

    async def close(self) -> None:
        """Close the database connection asynchronously."""
        if self.connection:
            await self.connection.close()
            self.connection = None
