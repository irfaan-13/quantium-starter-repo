#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Path to your virtual environment activation script
# Adjust this path according to your project structure and OS
VENV_PATH="C:\Users\george\Downloads\quantium-starter-repo\.venv\Scripts\activate"

if [ ! -f "$VENV_PATH" ]; then
    echo "Virtual environment activation script not found at $VENV_PATH"
    exit 1
fi

# Activate the virtual environment
source "$VENV_PATH"

# Run pytest and capture exit code
pytest -v
TEST_EXIT_CODE=$?

# Deactivate virtual environment
deactivate

# Exit with pytest's exit code (0 = success, 1+ = failure)
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "All tests passed."
    exit 0
else
    echo "Some tests failed."
    exit 1
fi