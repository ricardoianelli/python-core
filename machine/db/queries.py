CREATE_MACHINE_EVENTS_TABLE = """
CREATE TABLE IF NOT EXISTS machine_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    event_details TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

INSERT_MACHINE_EVENT = """
INSERT INTO machine_events (event_type, event_details) VALUES (?, ?);
"""

FETCH_MACHINE_EVENTS = """
SELECT * FROM machine_events ORDER BY timestamp DESC;
"""
