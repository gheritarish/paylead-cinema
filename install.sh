#!/bin/sh

echo "Creating environment"
python3.8 -m venv paylead
source ./paylead/bin/activate

echo "Installing dependencies..."
pip install -r ./requirements.txt

echo "Dependencies installed!"
