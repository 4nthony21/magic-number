"""
Uso:
  python scripts/inspect_db.py --db Annies.db --samples 5
"""

import argparse
import sqlite3
import pandas as pd
import os
import sys


def list_tables(conn):
    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    return [r[0] for r in cur.fetchall()]


def row_count(conn, table):
    cur = conn.execute(f"SELECT COUNT(*) FROM '{table}'")
    return cur.fetchone()[0]


def sample_rows(conn, table, limit=5):
    try:
        return pd.read_sql_query(f"SELECT * FROM '{table}' LIMIT {limit}", conn)
    except Exception as e:
        return None


def main():
    parser = argparse.ArgumentParser(description='Inspect SQLite DB')
    parser.add_argument('--db', '-d', default='Annies.db', help='Path to SQLite DB')
    parser.add_argument('--samples', '-s', type=int, default=5, help='Number of sample rows per table')
    args = parser.parse_args()

    db_path = args.db
    if not os.path.exists(db_path):
        print(f"Database not found: {db_path}")
        sys.exit(2)

    conn = sqlite3.connect(db_path)

    tables = list_tables(conn)
    if not tables:
        print(f"No tables found in {db_path}")
        conn.close()
        return

    print(f"Database: {db_path}\nTables found: {len(tables)}\n")

    for t in tables:
        try:
            cnt = row_count(conn, t)
        except Exception:
            cnt = 'error'
        print(f"- {t}: {cnt} rows")
        df = sample_rows(conn, t, args.samples)
        if df is None or df.empty:
            print("  (no sample available)\n")
        else:
            print(df.head(args.samples).to_string(index=False))
            print("\n")

    conn.close()


if __name__ == '__main__':
    main()
