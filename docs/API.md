# Script Description

## ETL/config.py
- Main variables:
  - `URLS`: list of pairs `[url, nombre_tabla]` used by `extract.py`.
  - `LOCAL_PATH`: destination folder for downloaded files.
  - `DATABASE_PATH`: path of the resulting SQLite file.
  - `TABLES`: list of table names to be loaded.

## ETL/extract.py
  - `download(url,path)`: download an HTTP resource to `path`. Use 'requests' with retries and logging.
  - `unzip(zip_path, dest_path)`: unzip file to `dest_path` and remove zip file.
  - `rename(name,new_name)`: rename files.

## ETL/schemas.py
- Defines `EXPECTED_COLUMNS` per files. Use in `tests/test_validate_schemas.py` to validate that CSVs contain the minimum required columns before loading.

## tests/
- `tests/test_validate_schemas.py`: light integration test that verifies the presence of expected columns in `Data/{table}.csv`.

## scripts/inspect_db.py
- Utility tool to list tables, counts, and samples from `Annies.db`.

## Integration notes
- If you want to use another database engine, replace the loading section that uses `pandas.to_sql`.
