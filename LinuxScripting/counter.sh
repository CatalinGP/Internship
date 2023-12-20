#!/bin/bash
# Count occurences of a string in a file

if [ "$#" -ne 2 ]; then
	echo "Usage: $0 file_name search_string"
	exit 1
fi

FILE_NAME=$1
SEARCH_STRING=$2

if [ ! -f "$FILE_NAME" ]; then
	echo "Error: File does not exist."
	exit 1
fi

COUNT=$(grep -o "$SEARCH_STRING" "$FILE_NAME" | wc -l )

echo "The string '$SEARCH_STRING' occurs $COUNT times in $FILE_NAME."
