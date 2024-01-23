# Filename: exercise4.py
# Language: Python

# Exercise 4: Mowesta

import pandas as pd
import urllib.request
import zipfile
import os
import sqlite3
import shutil

# Step 1: Download and Unzip Data
url = 'https://www.mowesta.com/data/measure/mowesta-dataset-20221107.zip'
zip_path = 'mowesta_dataset.zip'
urllib.request.urlretrieve(url, zip_path)

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall('mowesta_data')
os.remove(zip_path)

# Step 2: Reshape Data
data_path = 'mowesta_data/data.csv'

# Read the CSV with flexible handling of bad lines
try:
    df = pd.read_csv(data_path, delimiter=';', decimal=',', on_bad_lines='skip')
except Exception as e:
    print("Error reading the CSV file:", e)
    exit()

# Select and rename the required columns
df = df[['Geraet', 'Hersteller', 'Model', 'Monat', 'Temperatur in °C (DWD)', 'Batterietemperatur in °C', 'Geraet aktiv']]
df.rename(columns={'Temperatur in °C (DWD)': 'Temperatur', 'Batterietemperatur in °C': 'Batterietemperatur'}, inplace=True)

# Step 3: Transform Data
def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

df['Temperatur'] = df['Temperatur'].apply(celsius_to_fahrenheit)
df['Batterietemperatur'] = df['Batterietemperatur'].apply(celsius_to_fahrenheit)

# Step 4: Validate Data
df = df[df['Geraet'] > 0]

# Step 5: Write Data to SQLite Database
conn = sqlite3.connect('temperatures.sqlite')
df.to_sql('temperatures', conn, if_exists='replace', index=False, dtype={
    'Geraet': 'BIGINT',
    'Hersteller': 'TEXT',
    'Model': 'TEXT',
    'Monat': 'TEXT',
    'Temperatur': 'FLOAT',
    'Batterietemperatur': 'FLOAT',
    'Geraet aktiv': 'TEXT'
})
conn.close()

# Delete the mowesta_data folder
shutil.rmtree('mowesta_data')
