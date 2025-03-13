import asyncio
from datetime import datetime
from core.logging.logger_interface import LoggerInterface
from core.logging.log_repository import LogRepository
from core.backend.websocket_manager import WebSocketManager

class DatabaseLogger(LoggerInterface):
    """Logs messages to the database and handles database operations."""

    def __init__(self):
        self.repository = LogRepository()

    async def initialize(self):
        """Ensures the logs table exists and subscribes to WebSocket events."""
        await self.repository.initialize_database()

        # Subscribe to WebSocket messages
        WebSocketManager.subscribe_to_incoming("add_log", self.add_log)
        WebSocketManager.subscribe_to_incoming("fetch_logs", self.fetch_logs)
        WebSocketManager.subscribe_to_incoming("fetch_logs_by_level", self.fetch_logs_by_level)
        WebSocketManager.subscribe_to_incoming("delete_old_logs", self.delete_old_logs)
        WebSocketManager.subscribe_to_incoming("delete_log", self.delete_log)
        WebSocketManager.subscribe_to_incoming("clear_logs", self.clear_logs)

    async def log_async(self, log_level: str, message: str):
        """Logs a message asynchronously into the database."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await self.repository.add_log(log_level, message, timestamp)

        # Notify WebSocket clients
        await WebSocketManager.broadcast({
            "type": "new_log",
            "log_level": log_level,
            "message": message,
            "timestamp": timestamp
        })

    def log(self, log_level: str, message: str):
        """Logs a message synchronously into the database."""
        asyncio.run(self.log_async(log_level, message))
        
    async def add_log(self, message):
        """Handles adding a log from WebSocket events."""
        log_level = message.get("log_level", "INFO")
        log_message = message.get("message", "No message provided")
        await self.log_async(log_level, log_message)

    async def fetch_logs(self, message):
        """Handles fetching logs and sending them to the WebSocket client."""
        logs = await self.repository.get_logs()
        await WebSocketManager.broadcast({"type": "all_logs", "logs": logs})

    async def fetch_logs_by_level(self, message):
        """Fetch logs filtered by log level."""
        log_level = message.get("log_level", "INFO")
        logs = await self.repository.get_logs_by_level(log_level)
        await WebSocketManager.broadcast({"type": "filtered_logs", "logs": logs})

    async def delete_old_logs(self, message):
        """Deletes older logs while keeping the most recent ones."""
        max_entries = message.get("max_entries", 1000)
        await self.repository.delete_old_logs(max_entries)
        await WebSocketManager.broadcast({"type": "logs_deleted", "remaining_entries": max_entries})
    
    async def delete_log(self, message):
        """Deletes a log entry."""
        log_id = message.get("id")
        await self.repository.delete_log(log_id)
        await WebSocketManager.broadcast({"type": "log_deleted", "id": log_id})

    async def clear_logs(self, message):
        """Deletes all logs."""
        await self.repository.clear_logs()
        await WebSocketManager.broadcast({"type": "logs_cleared"})
