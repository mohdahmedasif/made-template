# project/tests/test_pipeline.py

import os
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
import pytest
from pipeline import download_kaggle_datasets, preprocess_and_migrate, fetch_and_preprocess_data, migrate_to_sqlite

@pytest.fixture
def sample_data():
    # Provide some sample data for testing
    data = {
        'data_source1': {
            'files': ['indexData.csv', 'indexInfo.csv'],
            'defined_function': 'preprocess_stock_data',
            'target_table': 'stock_exchange_data',
            'table_rule': 'replace'
        }
    }
    return data

def test_download_kaggle_datasets(sample_data, tmpdir):
    # Create a temporary directory for testing
    temp_dir = tmpdir.mkdir("test_data")

    # Modify the sample data to use the temporary directory
    sample_data['download_directory'] = temp_dir.strpath

    # Perform the test
    download_kaggle_datasets(sample_data)

    # Check if the files were downloaded to the correct location
    assert os.path.exists(os.path.join(temp_dir.strpath, 'data_source1', 'indexData.csv'))
    assert os.path.exists(os.path.join(temp_dir.strpath, 'data_source1', 'indexInfo.csv'))

def test_fetch_and_preprocess_data(sample_data, tmpdir):
    # Create a temporary directory for testing
    temp_dir = tmpdir.mkdir("test_data")

    # Modify the sample data to use the temporary directory
    sample_data['download_directory'] = temp_dir.strpath

    # Download data for testing
    download_kaggle_datasets(sample_data)

    # Fetch and preprocess data for testing
    data = fetch_and_preprocess_data(temp_dir.strpath, 'data_source1', ['indexData.csv', 'indexInfo.csv'], 'preprocess_stock_data')

    # Check if the returned data is a pandas DataFrame
    assert isinstance(data, pd.DataFrame)

    # Check if the DataFrame has the expected columns
    expected_columns = ['index', 'date', 'open', 'high', 'low', 'close', 'adj_close', 'volume', 'region', 'exchange', 'currency']
    assert all(column in data.columns for column in expected_columns)

def test_migrate_to_sqlite(sample_data, tmpdir):
    # Create a temporary database file for testing
    database_file = os.path.join(tmpdir.strpath, 'test_database.sqlite')

    # Modify the sample data to use the temporary database file
    sample_data['database_file'] = database_file

    # Fetch and preprocess data for testing
    data = fetch_and_preprocess_data(tmpdir.strpath, 'data_source1', ['indexData.csv', 'indexInfo.csv'], 'preprocess_stock_data')

    # Migrate data to SQLite for testing
    migrate_to_sqlite(data, database_file, 'stock_exchange_data', 'replace')

    # Check if the table exists in the SQLite database
    engine = create_engine(f'sqlite:///{database_file}')
    assert engine.has_table('stock_exchange_data')
