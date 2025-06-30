CREATE TABLE IF NOT EXISTS recalls (
    recall_number   TEXT PRIMARY KEY,
    brand_name      TEXT,
    generic_name    TEXT,
    classification  TEXT,
    reason_raw      TEXT,
    reason_ai       TEXT,
    recall_date     DATE
);

CREATE TABLE IF NOT EXISTS run_log (
    run_timestamp   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    rows_inserted   INTEGER
);
