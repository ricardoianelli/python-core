CREATE_MACHINE_EVENTS_TABLE = """
CREATE TABLE IF NOT EXISTS machine_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL CHECK(length(event_type) <= 255),
    event_details TEXT NOT NULL CHECK(length(event_details) <= 5000),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_TIMESTAMP_INDEX = """
CREATE INDEX IF NOT EXISTS idx_machine_events_timestamp ON machine_events(timestamp);
"""

INSERT_MACHINE_EVENT = """
INSERT INTO machine_events (event_type, event_details) VALUES (?, ?);
"""

FETCH_MACHINE_EVENTS = """
SELECT id, event_type, event_details, timestamp FROM machine_events ORDER BY timestamp DESC;
"""

CLEAR_MACHINE_EVENTS = """
DELETE FROM machine_events;
"""
