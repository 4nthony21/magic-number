# ETL Architecture

## Flow
1. `ETL/config.py` define las `URLS`, el `LOCAL_PATH` y `TABLES`.
2. `ETL/extract.py` downloads each ZIP file, extracts it, and renames the CSV according to the configuration.
3. `ETL/load.py` calls `extract.py` y, and, after extraction, loads each CSV into SQLite using `pandas`.

## Considerations
- Extraction: `ETL/extract.py` uses a `requests` session with retries and backoff, and logs activity using `logging`.
- Temporary storage: `Data/` is the local folder for extracted files (it is recreated for each extraction run).
- Validation: expected schemas were added to `ETL/schemas.py` and tests were added to `tests/` to validate CSV before loading.
- Loading: `pandas.DataFrame.to_sql` writes directly to the SQLite database (`Annies.db`) by default.
