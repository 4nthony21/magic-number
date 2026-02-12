import os
import pytest
import pandas as pd

from ETL.config import TABLES, LOCAL_PATH
from ETL.schemas import EXPECTED_COLUMNS


@pytest.mark.parametrize("table", TABLES)
def test_csv_has_expected_columns(table):
    """Ensure the CSV for `table` exists and contains the expected columns.

    This test is intended to run before loading into the DB so that
    schema issues are caught early.
    """
    csv_path = os.path.join(LOCAL_PATH, f"{table}.csv")

    assert os.path.exists(csv_path), (
        f"CSV for table '{table}' not found at {csv_path}. "
        "Run ETL/extract.py first to download and extract source files."
    )

    # read only header
    try:
        df = pd.read_csv(csv_path, nrows=0)
    except Exception as e:
        pytest.fail(f"Failed reading CSV header for {csv_path}: {e}")

    actual_cols = set(df.columns.tolist())
    expected = set(EXPECTED_COLUMNS.get(table, []))

    missing = expected - actual_cols
    assert not missing, f"Missing expected columns for {table}: {sorted(missing)}"
