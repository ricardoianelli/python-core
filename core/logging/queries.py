CREATE_LOGS_TABLE = """
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_level TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

INSERT_LOG = """
INSERT INTO logs (log_level, message, timestamp) VALUES (?, ?, ?);
"""

FETCH_ALL_LOGS = """
SELECT id, log_level, message, timestamp FROM logs ORDER BY id ASC;
"""

FETCH_LOGS_BY_LEVEL = """
SELECT id, log_level, message, timestamp FROM logs WHERE log_level = ? ORDER BY id ASC;
"""

DELETE_OLD_LOGS = """
DELETE FROM logs WHERE id NOT IN (
    SELECT id FROM logs ORDER BY id DESC LIMIT ?
);
"""

DELETE_LOG_BY_ID = """
DELETE FROM logs WHERE id = ?;
"""

CLEAR_ALL_LOGS = """
DELETE FROM logs;
"""
