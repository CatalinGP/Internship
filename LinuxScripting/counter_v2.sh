#!/bin/bash

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 search_string file1 [file2 ...]"
    exit 1
fi

SEARCH_STRING=$1

for FILE in "${@:2}"; do
    echo "Searching in $FILE:"

    # Check if file exists
    if [ ! -f "$FILE" ]; then
        echo "Error: File $FILE does not exist."
        continue
    fi

   
    COUNT=$(grep -c "$SEARCH_STRING" "$FILE")
    echo "Occurrences of '$SEARCH_STRING': $COUNT"
    echo "Lines found:"
    grep -n "$SEARCH_STRING" "$FILE"
    echo ""
done

