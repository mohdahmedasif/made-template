# Project Plan

## Title

Quantifying Market Sentiment: An In-Depth Analysis of Social Media and News Impact on Stock Prices

## Main Question

1. To what extent do sentiments expressed on social media and news impact stock prices?

## Description

In this project, we aim to explore the relationship between social media sentiment and news sentiment and their influence on stock prices. We'll perform sentiment analysis on a dataset of social media posts and news articles related to specific stocks and analyze their impact on stock price movements. By investigating this relationship, we aim to provide insights for investors and traders.

## Datasources

### Datasource1: Stock Price Data
* Metadata URL: https://www.kaggle.com/datasets/mattiuzc/stock-exchange-data/data
* Data URL: https://www.kaggle.com/datasets/mattiuzc/stock-exchange-data?select=indexData.csv
* Data Type: CSV
* Description: Daily price data for indexes tracking stock exchanges from all over the world (United States, China, Canada, Germany, Japan, and more). The data was all collected from Yahoo Finance, which had several decades of data available for most exchanges.

### Datasource2: News Data
* Metadata URL: https://www.kaggle.com/datasets/therohk/million-headlines
* Data URL: https://www.kaggle.com/datasets/therohk/million-headlines?select=abcnews-date-text.csv
* Data Type: CSV
* Description: This contains data of news headlines published over a period of nineteen years.Sourced from the reputable Australian news source ABC (Australian Broadcasting Corporation)

### Datasource3: News Data
* Metadata URL: https://www.kaggle.com/datasets/gpreda/bbc-news
* Data URL: https://www.kaggle.com/datasets/gpreda/bbc-news?select=bbc_news.csv
* Data Type: CSV
* Description: Self updating dataset. It collects RSS Feeds from BBC News using a Kernel. The Kernel is run with a fixed frequency and the dataset is updated using the output of the Notebook.

## Work Packages

1. Data Collection and Preprocessing [#1](https://github.com/mohdahmedasif/made-template/issues/1)
2. Sentiment Analysis on Social Media Data [#2](https://github.com/mohdahmedasif/made-template/issues/2)
3. Sentiment Analysis on News Articles Data [#3](https://github.com/mohdahmedasif/made-template/issues/3)
4. Integration of Sentiment Data with Stock Price Data [#4](https://github.com/mohdahmedasif/made-template/issues/4)
5. Statistical Analysis and Modeling [#5](https://github.com/mohdahmedasif/made-template/issues/5)
6. Visualization of Results [#6](https://github.com/mohdahmedasif/made-template/issues/6)
7. Final Report and Insights [#7](https://github.com/mohdahmedasif/made-template/issues/7)

# Data Integration Pipeline

This Python script automates the process of downloading datasets from Kaggle, preprocessing the data, and migrating it into an SQLite database. The pipeline includes fetching stock exchange data and news data from various Kaggle datasets.

## Prerequisites

1. **Kaggle Account and API Key:**
   - Ensure you have a Kaggle account.
   - Generate a Kaggle API key from your Kaggle account settings.
   - Place the Kaggle API key (`kaggle.json`) in the root directory of this project.

2. **Python Environment:**
   - Make sure you have Python installed (version 3.x is recommended).

## Setup

1. **Create a Virtual Environment (Optional):**
   - It's recommended to create a virtual environment before installing packages. Use the following commands:

     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```

2. **Install Required Packages:**
   - Install the required Python packages by running the following command in your terminal or command prompt:

     ```bash
     pip install -r requirements.txt
     ```


## Additional Information

- **Monitor Progress:**
   - The script will download datasets, preprocess the data, and migrate it into the SQLite database.
   - Progress updates will be printed in the console.

- **Downloaded Datasets Location:**
  - The downloaded datasets will be stored in the specified `download_directory` (default: '../data/raw').

- **SQLite Database:**
  - The preprocessed data will be stored in the SQLite database specified by `database_file`.

- **Handling Errors:**
  - If any errors occur during the process, an error message will be displayed in the console.

## Usage

### Run Pipeline Using `pipeline.sh`

   ```bash
   bash pipeline.sh
   ```
   
### Run System Test Using `tests.sh`
   
   ```bash
   bash tests.sh
   ```