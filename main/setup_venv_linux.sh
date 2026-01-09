#!/usr/bin/env bash

set -e



# Check if python is available

if ! command -v python3 >/dev/null 2>&1; then

    echo "Python is not found in PATH. Please install Python 3.10.11 and ensure it is available."

    exit 1

fi



# Get Python version (e.g. 3.10.11)

PYVER=$(python3 --version | awk '{print $2}')



MAJOR=$(echo "$PYVER" | cut -d. -f1)

MINOR=$(echo "$PYVER" | cut -d. -f2)



if [ "$MAJOR" -ne 3 ] || [ "$MINOR" -ne 10 ]; then

    echo "Python 3.10 is required. Found: $PYVER"

    exit 1

fi



echo "Creating virtual environment in 'venv'..."

python3 -m venv venv



if [ -f venv/bin/activate ]; then

    echo "Virtual environment created successfully."



    # Activate only for dependency installation

    source venv/bin/activate



    echo "Upgrading pip..."

    python -m pip install --upgrade pip



    if [ -f requirements.txt ]; then

        echo "Installing dependencies from requirements.txt..."

        pip install -r requirements.txt

    else

        echo "No requirements.txt found. Skipping package installation."

    fi



    deactivate

else

    echo "Failed to create virtual environment."

    exit 1

fi



echo

echo "Setup complete."

echo "To activate the environment, run:"

echo "  source venv/bin/activate"