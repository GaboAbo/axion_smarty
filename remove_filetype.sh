#!/bin/bash

# Check if file extension is provided
if [ -z "$1" ]; then
    echo "Usage: $0 file_extension (e.g. log, tmp, pyc)"
    exit 1
fi

EXT="$1"

# Find and delete all files with the given extension
echo "Removing all *.Identifier files from current and subdirectories..."

find . -type f -name "*.Identifier" -print -delete

echo "Done."
