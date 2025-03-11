from abc import ABC, abstractmethod

class LoggerInterface(ABC):
    """Abstract interface for logging implementations."""

    @abstractmethod
    async def log_async(self, log_level: str, message: str):
        """Logs a message asynchronously."""
        pass

    @abstractmethod
    def log(self, log_level: str, message: str):
        """Logs a message synchronously."""
        pass
