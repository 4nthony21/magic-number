## Usage

Step-by-step instructions for running the ETL pipeline included in this repository.

1) Enviroment

```bash
python -m venv venv
venv\Scripts\Activate.ps1  # PowerShell
pip install -r requirements.txt
```

2) Run complete pipeline

```bash
python ETL/load.py
```

3) Verify results

Use any SQLite client or `pandas` to inspect the tables created.

4) Customization
- Change `ETL/config.py` to modify URLs, table names, or local paths.
- If you want to run only the extraction: run `ETL/extract.py`.

5) Warnings
- The `extract.py` script deletes and recreates the `Data/` folder each time it runs.
   Make sure you don't have any unsaved files in it.


Inspect DB
----------------------------

A utility script is included to quickly inspect `Annies.db`:

```bash
python scripts/inspect_db.py --db Annies.db --samples 5
```

What it does:
- Lists the tables existing in the database.
- Shows the row count per table.
- Prints up to `--samples` sample rows per table using `pandas`.

This script is useful after running `ETL/load.py` to verify that the tables were loaded correctly and to review samples of the data.

Tests
-----

The tests are in the `tests/` folder and are run with `pytest`.

- `tests/test_validate_schemas.py` validates that the CSVs in `Data/` contain the expected columns according to `ETL/schemas.py`.
- To run the tests locally:

```bash
pip install -r requirements.txt
pytest -q
```

