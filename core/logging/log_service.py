import asyncio
from core.backend.websocket_manager import WebSocketManager
from core.logging.log_repository import LogRepository
from datetime import datetime

class LogService:
    """Handles all log-related actions and WebSocket subscriptions."""

    repository = LogRepository()
    
    @classmethod
    async def initialize(cls):
        await cls.repository.initialize_database()
        
        # Subscribe to WebSocket messages
        WebSocketManager.subscribe_to_incoming("add_log", cls.add_log)
        WebSocketManager.subscribe_to_incoming("fetch_logs", cls.fetch_logs)
        WebSocketManager.subscribe_to_incoming("fetch_logs_by_level", cls.fetch_logs_by_level)
        WebSocketManager.subscribe_to_incoming("delete_old_logs", cls.delete_old_logs)
        WebSocketManager.subscribe_to_incoming("delete_log", cls.delete_log)
        WebSocketManager.subscribe_to_incoming("clear_logs", cls.clear_logs)

    @classmethod
    def log(cls, text, log_level="INFO"):
        """Logs a message synchronously (for use in non-async functions)."""
        asyncio.run(cls.log_async(text, log_level))  # Calls async version safely

    @classmethod
    async def log_async(cls, text, log_level="INFO"):
        """Logs a message asynchronously."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await cls.repository.add_log(log_level, text, timestamp)

        # Notify WebSocket clients
        await WebSocketManager.broadcast({
            "type": "new_log",
            "log_level": log_level,
            "message": text,
            "timestamp": timestamp
        })
    
    @classmethod
    async def add_log(cls, message):
        """Handles adding a new log from WebSocket."""
        log_message = message.get("message", "No message provided")
        log_level = message.get("log_level", "INFO")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Save to database and get the real timestamp
        await cls.repository.add_log(log_level, log_message, timestamp)

        # Notify all clients
        await WebSocketManager.broadcast({
            "type": "new_log",
            "log_level": log_level,
            "message": log_message,
            "timestamp": timestamp  # Send the real timestamp
        })


    @classmethod
    async def fetch_logs(cls, message):
        """Handles fetching logs and sending them to the WebSocket client."""
        logs = await cls.repository.get_logs()
        await WebSocketManager.broadcast({"type": "all_logs", "logs": logs})

    @classmethod
    async def fetch_logs_by_level(cls, message):
        """Fetch logs filtered by log level."""
        log_level = message.get("log_level", "INFO")
        logs = await cls.repository.get_logs_by_level(log_level)
        await WebSocketManager.broadcast({"type": "filtered_logs", "logs": logs})

    @classmethod
    async def delete_old_logs(cls, message):
        """Deletes older logs while keeping the most recent ones."""
        max_entries = message.get("max_entries", 1000)
        await cls.repository.delete_old_logs(max_entries)
        await WebSocketManager.broadcast({"type": "logs_deleted", "remaining_entries": max_entries})
       
    @classmethod 
    async def delete_log(cls, message):
        """Deletes a log entry."""
        log_id = message.get("id")
        await cls.repository.delete_log(log_id)
        await WebSocketManager.broadcast({"type": "log_deleted", "id": log_id})

    @classmethod
    async def clear_logs(cls, message):
        """Deletes all logs."""
        await cls.repository.clear_logs()
        await WebSocketManager.broadcast({"type": "logs_cleared"})
