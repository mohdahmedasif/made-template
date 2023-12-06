#!/bin/bash

printf "Installing required dependencies\n"
pip install -r requirements.txt

printf "Running the test cases\n"
python -m pytest tests/sys_testing.py