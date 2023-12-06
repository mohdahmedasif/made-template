#!/bin/bash

printf "Installing required dependencies\n"
pip install -r requirements.txt

printf "Running the pipeline\n"
python3 pipeline.py