/*
   Each row in this table contains the relevant metadata for a log entry
 */
CREATE TABLE IF NOT EXISTS logs (
  timestamp_utc DATETIME NOT NULL,
  event_id INTEGER NOT NULL,
  description TEXT,
  details TEXT,
  event_source TEXT NOT NULL,
  event_log TEXT NOT NULL,
  session_id INTEGER NOT NULL,
  account TEXT NOT NULL,
  computer_name TEXT NOT NULL,
  record_number INTEGER NOT NULL,
  recovered BOOLEAN NOT NULL,
  source_file_hash TEXT NOT NULL,
  record_hash TEXT NOT NULL,
  FOREIGN KEY(source_file_hash) REFERENCES source_files(hash)
);
/*
    This table contains a row for each file which has been parsed for event logs.
 */
CREATE TABLE IF NOT EXISTS source_files (
  file_name TEXT NOT NULL,
  hash TEXT NOT NULL UNIQUE,
  import_timestamp DATETIME NOT NULL,
  computer_name TEXT
);