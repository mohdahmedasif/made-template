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

# Manually read and process the CSV file
data = []
with open(data_path, 'r') as file:
    for line in file:
        fields = line.strip().split(';')
        # Extract only the first 7 fields
        if len(fields) >= 7:
            data.append(fields[:7])

# Create DataFrame from the processed data
columns = ['Geraet', 'Hersteller', 'Model', 'Monat', 'Temperatur in °C (DWD)', 'Batterietemperatur in °C', 'Geraet aktiv']
df = pd.DataFrame(data, columns=columns)

# Convert numeric columns from string to float
df['Geraet'] = pd.to_numeric(df['Geraet'], errors='coerce')
df['Temperatur in °C (DWD)'] = pd.to_numeric(df['Temperatur in °C (DWD)'].str.replace(',', '.'), errors='coerce')
df['Batterietemperatur in °C'] = pd.to_numeric(df['Batterietemperatur in °C'].str.replace(',', '.'), errors='coerce')

# Rename columns
df.rename(columns={'Temperatur in °C (DWD)': 'Temperatur', 'Batterietemperatur in °C': 'Batterietemperatur'}, inplace=True)

# Step 3: Transform Data
def celsius_to_fahrenheit(celsius):
    return round((celsius * 9/5) + 32, 2)

df['Temperatur'] = df['Temperatur'].apply(celsius_to_fahrenheit)
df['Batterietemperatur'] = df['Batterietemperatur'].apply(celsius_to_fahrenheit)

# Step 4: Validate Data
df.dropna(inplace=True)  # Remove rows with missing values
df = df[df['Geraet'] > 0]

# Step 5: Write Data to SQLite Database
conn = sqlite3.connect('temperatures.sqlite')
df.to_sql('temperatures', conn, if_exists='replace', index=False, dtype={
    'Geraet': 'INTEGER',
    'Hersteller': 'TEXT',
    'Model': 'TEXT',
    'Monat': 'INTEGER',
    'Temperatur': 'REAL',
    'Batterietemperatur': 'REAL',
    'Geraet aktiv': 'TEXT'
})
conn.close()

# Delete the mowesta_data folder
shutil.rmtree('mowesta_data')
