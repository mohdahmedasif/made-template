# Filename: exercise4.py
# Language: Python

# Exercise 4: Mowesta

import os
import zipfile
import sqlalchemy
import urllib.request
import pandas as pd
import shutil

# Define the temperature conversion function
def celsius_to_fahrenheit(temp_cels):
    return (temp_cels * 9 / 5) + 32

# Step 1: Download and Unzip Data
URL = "https://www.mowesta.com/data/measure/mowesta-dataset-20221107.zip"
urllib.request.urlretrieve(URL, "data.zip")

with zipfile.ZipFile('data.zip', 'r') as zip_ref:
    zip_ref.extractall("mowesta_data")

# Step 2: Load and Transform Data
fields = ["Geraet", "Hersteller", "Model", "Monat", "Temperatur in °C (DWD)", "Batterietemperatur in °C", "Geraet aktiv"]
df = pd.read_csv('mowesta_data/data.csv', sep=";", usecols=fields, encoding='utf-8', decimal=",")
df.rename(columns={"Temperatur in °C (DWD)": "Temperatur", "Batterietemperatur in °C": "Batterietemperatur"}, inplace=True)

# Apply temperature conversion
df['Temperatur'] = celsius_to_fahrenheit(df['Temperatur'])
df['Batterietemperatur'] = celsius_to_fahrenheit(df['Batterietemperatur'])

# Step 3: Validate Data
df = df[df['Geraet'] > 0]
df = df[(df['Monat'] >= 1) & (df['Monat'] <= 12)]
df = df[(df['Temperatur'] >= -459.67) & (df['Temperatur'] <= 212)]
df = df[(df['Batterietemperatur'] >= -459.67) & (df['Batterietemperatur'] <= 212)]
valid_gear_aktiv_values = ["Ja", "Nein"]
df = df[df['Geraet aktiv'].isin(valid_gear_aktiv_values)]

# Step 4: Write Data to SQLite Database
engine = sqlalchemy.create_engine('sqlite:///temperatures.sqlite')
df.to_sql('temperatures', engine, if_exists='replace', index=False, dtype={
    "Geraet": sqlalchemy.BIGINT,
    "Hersteller": sqlalchemy.TEXT,
    "Model": sqlalchemy.TEXT,
    "Monat": sqlalchemy.BIGINT,
    "Temperatur": sqlalchemy.FLOAT,
    "Batterietemperatur": sqlalchemy.FLOAT,
    "Geraet aktiv": sqlalchemy.TEXT,
})

# Cleanup: Delete downloaded files and extracted folder
os.remove("data.zip")
shutil.rmtree("mowesta_data")
