import os
from datetime import datetime
from subprocess import run, PIPE
from sqlalchemy import create_engine, text
import pytest

def run_data_pipeline():
    try:
        # Run the data pipeline script
        result = run(["python", "pipeline.py"], stdout=PIPE, stderr=PIPE, text=True)
        print(result.stdout)
        print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error: {e}")
        return False

@pytest.mark.failure
def test_output_files_exist():
    # Define expected output file paths
    expected_output_files = [
        '../data/raw/stock_exchange_data.csv',
        '../data/raw/analysed_news.csv'
    ]

    # Check if each expected output file exists
    for file_path in expected_output_files:
        assert os.path.exists(file_path), f"Error: Output file {file_path} not found."

@pytest.mark.success
def test_sqlite_output():
    # Define the path to the SQLite database file
    database_file = '../data/made-project.sqlite'

    # Check if the SQLite database file exists
    assert os.path.exists(database_file), f"Error: SQLite database file {database_file} not found."

    # Connect to the SQLite database
    engine = create_engine(f'sqlite:///{database_file}')

    # Check if the required tables exist in the database
    with engine.connect() as connection:
        # Use SQLAlchemy's text construct to represent the SQL statement
        sql_statement = text("SELECT name FROM sqlite_master WHERE type='table';")

        # Execute the SQL statement and fetch all results
        tables = connection.execute(sql_statement).fetchall()

        expected_tables = ['stock_exchange_data', 'analysed_news']

        for table in expected_tables:
            assert (table,) in tables, f"Error: Table {table} not found in the SQLite database."
