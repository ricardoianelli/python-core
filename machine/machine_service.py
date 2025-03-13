from core.database.clients.sqlite_client import SQLiteClient
from core.logging.log_service import LogService
from machine.db.machine_repository import MachineRepository

class MachineService:
    """ Manages the lifecycle of the machine. """

    def __init__(self):
        self.running = False
        self.repository: MachineRepository = MachineRepository(SQLiteClient())

    async def initialize(self):
        """ Runs the full machine startup sequence asynchronously. """
        await LogService.log_async("Initializing machine.")
        
        #Still working on this
        await self.repository.initialize_database()
        
    
    async def shutdown(self):
        """ Runs the shutdown sequence asynchronously. """
        await LogService.log_async("Shutting down machine.")
        
