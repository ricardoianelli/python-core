from abc import ABC, abstractmethod
from typing import Any, List, Dict

class DatabaseClient(ABC):
    @abstractmethod
    async def connect(self, db_path: str = "app.db") -> None:
        """Connect to the database asynchronously."""
        pass

    @abstractmethod
    async def execute(self, query: str, params: tuple = ()) -> None:
        """Execute a query asynchronously."""
        pass

    @abstractmethod
    async def fetch_one(self, query: str, params: tuple = ()) -> Any:
        """Fetch a single record asynchronously."""
        pass

    @abstractmethod
    async def fetch_all(self, query: str, params: tuple = ()) -> List[Dict]:
        """Fetch multiple records asynchronously."""
        pass

    @abstractmethod
    async def close(self) -> None:
        """Close the database connection asynchronously."""
        pass
