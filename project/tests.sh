#!/bin/bash

printf "Installing required dependencies\n"
#pip install -r requirements.txt

printf "Running the pipeline\n"
##python3 pipeline.py

printf "Running the test cases\n"
python -m pytest tests/sys_testing.py