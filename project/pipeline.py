import os
import zipfile
import pandas as pd
from datetime import datetime
from database import create_tables
from sentiment import analyze_sentiment

# Set the Kaggle API configuration directory to a writable location
os.environ['KAGGLE_CONFIG_DIR'] = './'

from kaggle.api.kaggle_api_extended import KaggleApi
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

def download_kaggle_datasets(config):
    api = KaggleApi()
    api.authenticate()

    for source, source_config in config.items():
        # Skip non-dataset configuration entries
        if source in ['download_directory', 'database_file']:
            continue

        dataset_url = source_config['dataset_url']
        download_dir = os.path.join(config['download_directory'], source)

        # Create subdirectory for each dataset
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        # Download only the specified files for each dataset
        for file in source_config['files']:
            api.dataset_download_file(dataset_url, file, path=download_dir)

        # Unzip downloaded files
        zip_files = [file for file in os.listdir(download_dir) if file.endswith('.zip')]
        for zip_file in zip_files:
            zip_path = os.path.join(download_dir, zip_file)
            extract_zip(zip_path, download_dir)
            os.remove(zip_path)

def extract_zip(zip_file, extract_path):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

def preprocess_and_migrate(config):
    download_dir = config['download_directory']
    database_file = config['database_file']

    for source, source_config in config.items():
        # Skip non-dataset configuration entries
        if source in ['download_directory', 'database_file']:
            continue

        files = source_config['files']
        defined_function = source_config['defined_function']
        target_table = source_config['target_table']
        table_rule = source_config['table_rule']

        # Fetch and preprocess data based on the defined function
        data = fetch_and_preprocess_data(download_dir, source, files, defined_function)

        # Transfer the preprocessed data to SQLite
        migrate_to_sqlite(data, database_file, target_table, table_rule)

def fetch_and_preprocess_data(download_dir, source, files, defined_function):
    # List files in the download directory
    dataframes = []

    for file in files:
        # Fetch data for each file
        file_path = os.path.join(download_dir, source, file)
        dataframes.append(pd.read_csv(file_path)) 

    # Dynamically call the preprocess function
    preprocess_function = globals()[defined_function]
    preprocessed_data = preprocess_function(dataframes)

    return preprocessed_data

def preprocess_stock_data(dataframes):
    print("Pre-process Stock Data - Source 1 (" + datetime.now().strftime("%H:%M:%S") + ")")

    if len(dataframes) != 2:
        raise ValueError("Expected 2 dataframes for stock data preprocessing")

    # Rename columns for better clarity
    index_data, index_info = dataframes[0], dataframes[1]
    index_data.columns = ['Index', 'Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    index_info.columns = ['Region', 'Exchange', 'Index', 'Currency']

    # Merge dataframes on 'Index'
    merged_data = pd.merge(index_data, index_info, on='Index', how='inner')

    # Convert 'Date' to datetime format
    merged_data['Date'] = pd.to_datetime(merged_data['Date'])

    # Rename columns as per the specified structure
    merged_data = merged_data.rename(columns={
        'Index': 'index',
        'Currency': 'currency',
        'Exchange': 'exchange',
        'Region': 'region',
        'Date': 'date',
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Adj Close': 'adj_close',
        'Volume': 'volume'
    })

    return merged_data

def preprocess_source2_news(dataframes):
    print("Pre-process News Data - Source 2 (" + datetime.now().strftime("%H:%M:%S") + ")")

    # Rename columns for better clarity
    bbc_news = dataframes[0]
    bbc_news.columns = ['title', 'pubDate', 'guid', 'link', 'description']
    
    # Drop columns as per the specified structure
    bbc_news = bbc_news.drop(columns=['guid'])
    bbc_news = bbc_news.drop(columns=['link'])

    # Rename columns as per the specified structure
    bbc_news = bbc_news.rename(columns={
        'title': 'title',
        'pubDate': 'date',
        'description': 'description'
    })

    bbc_news['date'] = pd.to_datetime(bbc_news['date'], format='%a, %d %b %Y %H:%M:%S %Z', errors='coerce')
    bbc_news['sentiment_compound'] = bbc_news['title'].apply(analyze_sentiment)
    bbc_news['keywords'] = ''
    bbc_news['source'] = '2'

    return bbc_news

def preprocess_source3_news(dataframes):
    print("Pre-process News Data - Source 3 (" + datetime.now().strftime("%H:%M:%S") + ")")

    # Rename columns for better clarity
    headlines = dataframes[0]
    headlines.columns = ['publish_date', 'headline_text']
    
    # Rename columns as per the specified structure
    headlines = headlines.rename(columns={
        'headline_text': 'title',
        'publish_date': 'date'
    })

    headlines['date'] = pd.to_datetime(headlines['date'], format='%Y%m%d', errors='coerce')
    headlines['sentiment_compound'] = headlines['title'].apply(analyze_sentiment)
    headlines['keywords'] = ''
    headlines['source'] = '3'

    return headlines

def migrate_to_sqlite(data, database_file, table_name, table_rule):
    # Create SQLite engine
    engine = create_engine(f'sqlite:///{database_file}')

    # Transfer the preprocessed data to SQLite
    data.to_sql(table_name, engine, index=False, if_exists=table_rule)


def pipeline(config):
    download_kaggle_datasets(config)
    preprocess_and_migrate(config)

if __name__ == '__main__':

    database_file = '../data/made-project.sqlite'

    kaggle_datasets = {
        # https://www.kaggle.com/datasets/mattiuzc/stock-exchange-data
        'data_source1': {
            'dataset_url': 'mattiuzc/stock-exchange-data',
            'files': [
                'indexData.csv',
                'indexInfo.csv'
            ],
            'defined_function': 'preprocess_stock_data',
            'target_table': 'stock_exchange_data',
            'table_rule' : 'replace'
        },

        # https://www.kaggle.com/datasets/gpreda/bbc-news
        'data_source2': {
            'dataset_url': 'gpreda/bbc-news',
            'files': {
                'bbc_news.csv'
            },
            'defined_function': 'preprocess_source2_news',
            'target_table': 'analysed_news',
            'table_rule' : 'replace'
        },

        # https://www.kaggle.com/datasets/therohk/million-headlines
        'data_source3': {
            'dataset_url': 'therohk/million-headlines',
            'files': {
                'abcnews-date-text.csv'
            },
            'defined_function': 'preprocess_source3_news',
            'target_table': 'analysed_news',
             'table_rule' : 'append'
        },

        'download_directory': '../data/raw',
        'database_file': database_file
    }

try:
    pipeline(config=kaggle_datasets)
    print("Completed Successfully (" + datetime.now().strftime("%H:%M:%S") + ")")

except OperationalError as e:
    print(f"Error: {e}")