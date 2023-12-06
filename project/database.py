from sqlalchemy import create_engine, Column, Integer, String, Float, Date, MetaData, Table

def create_tables(engine, database_file):
    metadata = MetaData()

    # Define the stock_exchange_data table
    stock_exchange_data = Table(
        'stock_exchange_data', metadata,
        Column('index', String, primary_key=True),
        Column('currency', String),
        Column('exchange', String),
        Column('region', String),
        Column('date', Date),
        Column('open', Float),
        Column('high', Float),
        Column('low', Float),
        Column('close', Float),
        Column('adj_close', Float),
        Column('volume', Float)
    )

    # Define the analysed_news table
    analysed_news = Table(
        'analysed_news', metadata,
        Column('source', Integer, primary_key=True),
        Column('date', Date),
        Column('title', String),
        Column('description', String),
        Column('sentiment_compound', Float),
        Column('keywords', String)
    )

    # Drop tables if they exist
    stock_exchange_data.drop(engine, checkfirst=True)
    analysed_news.drop(engine, checkfirst=True)

    # Create tables
    metadata.create_all(engine)

    print('Tables Created Successfully')