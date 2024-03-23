#!/bin/bash

# Check if a project name was passed as an argument
if [ "$#" -ne 1 ]; then
    echo "Usage: install-app <project_name>"
    exit 1
fi

PROJECT_NAME="$1"

# Check for exported env var (if is empty)
if [[ -z "$REPO_ROOT" ]]; then
	echo "Project root not set"
	echo "Run from projects root dir 'source ./scripts/setup.sh'"
	exit 1
fi

# Define the path to the project and virtual environment based on the argument
PROJECT_DIR="$REPO_ROOT/projects/$PROJECT_NAME"
VENV_PATH="$PROJECT_DIR/venv"

# Check if the project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo "Project directory '$PROJECT_DIR' not found."
    exit 1
fi

# Check if the virtual environment directory exists
if [ ! -d "$VENV_PATH" ]; then
    echo "Virtual environment not found for project $PROJECT_NAME. Creating one now..."
    # Create the virtual environment
    python3 -m venv "$VENV_PATH"
fi

echo "Activating virtual environment for project $PROJECT_NAME..."
# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Check for requirements.txt and install dependencies if it exists
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    cd $PROJECT_DIR
    pip install -r "requirements.txt"
else
    echo "No requirements.txt found. Skipping dependency installation. Exiting..."
    deactivate
    exit 1
fi

