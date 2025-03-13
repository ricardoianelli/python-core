CREATE_LOGS_TABLE = """
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_level TEXT NOT NULL CHECK(log_level IN ('INFO', 'WARNING', 'ERROR')),
    message TEXT NOT NULL CHECK(length(message) <= 5000),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_TIMESTAMP_INDEX = """
CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON logs(timestamp);
"""

INSERT_LOG = """
INSERT INTO logs (log_level, message, timestamp) VALUES (?, ?, ?);
"""

FETCH_ALL_LOGS = """
SELECT id, log_level, message, timestamp FROM logs ORDER BY timestamp DESC;
"""

FETCH_LOGS_BY_LEVEL = """
SELECT id, log_level, message, timestamp FROM logs WHERE log_level = ? ORDER BY timestamp DESC;
"""

DELETE_OLD_LOGS = """
DELETE FROM logs WHERE id NOT IN (
    SELECT id FROM logs ORDER BY timestamp DESC LIMIT ?
);
"""

DELETE_LOG_BY_ID = """
DELETE FROM logs WHERE id = ?;
"""

CLEAR_ALL_LOGS = """
DELETE FROM logs;
"""
