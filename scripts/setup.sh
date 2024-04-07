#!/bin/bash

# Attempt to find the repository root by looking for a .git directory
find_repo_root() {
    local current_dir=$(pwd)
    while [[ "$current_dir" != "/" ]]; do
        if [[ -d "$current_dir/.git" ]]; then
            echo "$current_dir"
            return
        fi
        current_dir=$(dirname "$current_dir")
    done
    echo "Repository root not found." >&2
    exit 1
}

REPO_ROOT=$(find_repo_root)

# Export the REPO_ROOT variable
export REPO_ROOT
export DEBUG_MODE="1"

start_project() {
    if [[ -z "$REPO_ROOT" ]]; then
        echo "Repository root not set. Run 'source scripts/setup.sh' first."
        return 1
    fi
    bash "$REPO_ROOT/scripts/start.sh" "$@"
}

install_project() {
    if [[ -z "$REPO_ROOT" ]]; then
        echo "Repository root not set. Run 'scripts/setup.sh' first."
        return 1
    fi
    bash "$REPO_ROOT/scripts/install.sh" "$@"
}

# Set session-long variables
alias start-app=start_project
alias install-app=install_project
alias win-start="$REPO_ROOT/scripts/win-start.sh"



