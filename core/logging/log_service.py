import json
from core.backend.websocket_manager import WebSocketManager
from core.logging.log_repository import LogRepository

class LogService:
    """Handles all log-related actions and WebSocket subscriptions."""

    def __init__(self):
        self.repository = LogRepository()

        # Ensure database is initialized
        WebSocketManager.subscribe_to_incoming("initialize_logs", self.initialize_db)

        # Subscribe to WebSocket messages
        WebSocketManager.subscribe_to_incoming("add_log", self.add_log)
        WebSocketManager.subscribe_to_incoming("fetch_logs", self.fetch_logs)
        WebSocketManager.subscribe_to_incoming("fetch_logs_by_level", self.fetch_logs_by_level)
        WebSocketManager.subscribe_to_incoming("delete_old_logs", self.delete_old_logs)

    async def initialize_db(self, message):
        """Ensures the database is ready before any logging operations."""
        await self.repository.initialize_database()

    async def add_log(self, message):
        """Handles adding a new log from WebSocket."""
        log_message = message.get("message", "No message provided")
        log_level = message.get("log_level", "INFO")
        await self.repository.add_log(log_level, log_message)

        # Notify all clients that a new log was added
        await WebSocketManager.broadcast({
            "type": "new_log",
            "log_level": log_level,
            "message": log_message,
            "timestamp": "Just now"
        })

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
