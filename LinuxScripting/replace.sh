#!/bin/bash

INPUT_FILE="log.txt"
OUTPUT_FILE="update_log.txt"
REPLACEMENT="A U T O M A T I O N"

if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: File $INPUT_FILE does not exist."
    exit 1
fi

> "$OUTPUT_FILE"


for i in {63..69}; do
    OLD_WORD=$(sed -n "${i}p" "$INPUT_FILE" | awk '{print $6}')
    
    sed -i "${i}s/\b$OLD_WORD\b/$REPLACEMENT/" "$INPUT_FILE"
    
    echo "$OLD_WORD was replaced with the letters: [A, U, T, O, M, A, T, I, O, N]" >> "$OUTPUT_FILE"
done

cat "$OUTPUT_FILE"

