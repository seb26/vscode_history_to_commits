#!/bin/bash

# Directory containing the files
DIR=$1

# Regex pattern to capture filename, date, and extension
pattern='^(?<filename>.*)(?<date>_\d{14})\.(?<ext>.*)$'

# Loop through each file in the directory
for file in "$DIR"/*; do
    echo "Working on: $file"
    # Get the base name of the file
    basefile=$(basename "$file")
    
    if [[ $basefile =~ $pattern ]]; then
        filename="${BASH_REMATCH[1]}"
        date="${BASH_REMATCH[2]}"
        ext="${BASH_REMATCH[3]}"
        
        # Process date to ISO 8601 format
        git_date=$(date -d "${date:1:4}-${date:5:2}-${date:7:2}T${date:9:2}:${date:11:2}:${date:13:2}" --iso-8601=seconds)
        
        # Write the contents of the file to ./filename
        cat "$file" > "./$filename"
        
        # Git add and commit with the processed date
        git add -p "./$filename"
        git commit -v --date "$git_date" -m "Commit for $filename"
    else
        echo "No match: $file - Basefile: $basefile"
    fi
done