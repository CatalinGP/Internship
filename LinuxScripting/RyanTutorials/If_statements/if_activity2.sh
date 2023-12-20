#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Usage: $0 <file_path>"
	exit 1
fi

file_path="$1"

if [ ! -e "$file_path" ]; then
	echo "File does not exist: $file_path"
	exit 1
fi

if [ -x "$file_path" ]; then
	echo "The file $file_path is executable."
else
	echo "The file $file_path is not executable."
fi

if [ -w "$file_path" ]; then
	echo "The file $file_path is writable."
else
	echo "The file $file_path is not writable."
fi

