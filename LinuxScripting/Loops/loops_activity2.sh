#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Usage: $0 <directory_path>"
	exit 1
fi

directory="$1"

if [ ! -d "$directory" ]; then
	echo "Directory does not exist: $directory"
	exit 1
fi

for entry in "$directory"/*; do
	if [ -f "$entry" ]; then
		size=$(stat -c %s "$entry")
		echo "File: $entry, Size: $size bytes"
	elif [ -d "$entry" ]; then
		count=$(ls -A "$entry" | wc -l)
		echo "Directory: $entry, Items: $count"
	fi
done
