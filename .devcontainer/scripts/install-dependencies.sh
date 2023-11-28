#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Function to check if a command exists and its version is appropriate
command_exists() {
    type "$1" &> /dev/null
}

# Function to check Python and pip versions
check_python() {
    if ! command_exists python3; then
        echo "Python 3 is not installed."
        exit 1
    fi

    if ! python3 -m pip --version; then
        echo "pip for Python 3 is not installed."
        exit 1
    fi
}

# Function to check Node.js and npm versions
check_node() {
    if ! command_exists node; then
        echo "Node.js is not installed."
        exit 1
    fi

    if ! command_exists npm; then
        echo "npm is not installed."
        exit 1
    fi
}

# Install Python dependencies
check_python
echo "Installing Python dependencies..."
python3 -m pip install awscli-local

# Install Node.js dependencies
check_node
echo "Installing Node.js dependencies..."
#npm install -g aws-cdk
#npm install -g aws-cdk-local

echo "Installation of dependencies is complete."
