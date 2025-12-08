#!/bin/bash
# Helper script to run the newsletter with virtual environment activated

cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Run the newsletter script with all arguments passed through
python main.py "$@"



