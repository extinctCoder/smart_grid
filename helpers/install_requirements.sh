#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Determine the directory where this script is located.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# The root directory is assumed to be the parent of the script directory.
ROOT_DIR="$SCRIPT_DIR/.."

# List of requirements files to install, located at the project root.
REQ_FILES=(
  "requirements.ps_sim.txt"
  "requirements.m2i.txt"
)

# Loop through each requirements file and install if it exists.
for req in "${REQ_FILES[@]}"; do
  REQ_PATH="$ROOT_DIR/$req"
  if [ -f "$REQ_PATH" ]; then
    echo "Installing dependencies from $REQ_PATH..."
    pip install -r "$REQ_PATH"
  else
    echo "Warning: $REQ_PATH not found, skipping."
  fi
done

echo "All requirements installed."
