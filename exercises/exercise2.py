# Filename: exercise2.py
# Language: Python

# Exercise 2: Trainstops

import pandas as pd
import sqlalchemy

# Extracting CSV file from given file URL
url = 'https://download-data.deutschebahn.com/static/datasets/haltestellen/D_Bahnhof_2020_alle.CSV'

# Attempting to extract data from CSV
try:
    df = pd.read_csv(url, sep=';', decimal=',')
except Exception as e:
    raise Exception(f'Error occurred while extracting csv from given url {url}: {e}')

# Checking if data extraction was successful
if df is None:
    raise Exception(f'Error occurred while extracting csv from given url {url}')

# Removing column: Status
df = df.drop(columns=['Status'])

# Removing entries that do not have valid values
#Valid "Verkehr" values are "FV", "RV", "nur DPN"
#Valid "Laenge", "Breite" values are geographic coordinate system values between and including -90 and 90
#Valid "IFOPT" values follow this pattern: <exactly two characters>:<any amount of numbers>:<any amount of numbers><optionally another colon followed by any amount of numbers>
#Empty cells are considered invalid

valid_values_condition = (
    (df['Verkehr'].isin(['FV', 'RV', 'nur DPN'])) &
    (df['Laenge'].between(-90, 90, inclusive='both')) &
    (df['Breite'].between(-90, 90, inclusive='both')) &
    (df['IFOPT'].str.match(r'^[a-zA-Z]{2}:\d+:\d+(\:\d+)?$')) &
    (df.notnull().all(axis=1))
)
df = df[valid_values_condition]

# Migrating the data into sqlite database
df.to_sql('trainstops', 'sqlite:///trainstops.sqlite', if_exists='replace', index=False, dtype={
    "EVA_NR": sqlalchemy.BIGINT,
    "DS100": sqlalchemy.TEXT,
    "IFOPT": sqlalchemy.TEXT,
    "NAME": sqlalchemy.TEXT,
    "Verkehr": sqlalchemy.TEXT,
    "Laenge": sqlalchemy.FLOAT,
    "Breite": sqlalchemy.FLOAT,
    "Betreiber_Name": sqlalchemy.TEXT,
    "Betreiber_Nr": sqlalchemy.BIGINT
})
