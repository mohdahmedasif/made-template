# Filename: exercise4.py
# Language: Python

# Exercise 4: Mowesta

import os
import shutil
import zipfile
import sqlalchemy
import urllib.request
import pandas as pd

url = "https://www.mowesta.com/data/measure/mowesta-dataset-20221107.zip"
zip_path = 'mowesta_dataset.zip'
data_path = 'mowesta_data/data.csv'

urllib.request.urlretrieve(url, zip_path)

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall('mowesta_data')
os.remove(zip_path)

fields = ["Geraet", "Hersteller", "Model", "Monat", "Temperatur in °C (DWD)", "Batterietemperatur in °C", "Geraet aktiv"]
df = pd.read_csv(data_path, sep=";", index_col=False, usecols=fields, encoding='utf-8', decimal=",")
df.rename(columns={"Temperatur in °C (DWD)": "Temperatur", "Batterietemperatur in °C": "Batterietemperatur"}, inplace=True)

def celsius_to_fahrenheit(temp_cels):
    return (temp_cels * 9 / 5) + 32

df['Temperatur'] = celsius_to_fahrenheit(df['Temperatur'])
df['Batterietemperatur'] = celsius_to_fahrenheit(df['Batterietemperatur'])

# Validate data
df = df.loc[df['Geraet'] > 0]
df = df.loc[(df['Monat'] >= 1) & (df['Monat'] <= 12)]
df = df.loc[(df['Temperatur'] >= -459.67) & (df['Temperatur'] <= 212)]
df = df.loc[(df['Batterietemperatur'] >= -459.67) & (df['Batterietemperatur'] <= 212)]
valid_gear_aktiv_values = ["Ja", "Nein"]
df = df.loc[(df['Geraet aktiv'].isin(valid_gear_aktiv_values))]

df.to_sql('temperatures', 'sqlite:///temperatures.sqlite', if_exists='replace', index=False, dtype={
    "Geraet": sqlalchemy.BIGINT,
    "Hersteller": sqlalchemy.TEXT,
    "Model": sqlalchemy.TEXT,
    "Monat": sqlalchemy.BIGINT,
    "Temperatur": sqlalchemy.FLOAT,
    "Batterietemperatur": sqlalchemy.FLOAT,
    "Geraet aktiv": sqlalchemy.TEXT,
})

# Delete the mowesta_data folder
shutil.rmtree('mowesta_data')