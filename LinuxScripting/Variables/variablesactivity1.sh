#!/bin/bash

# Check if at least one argument is provided
if [ $# -eq 0 ]; then
	echo "Usage: $0 <arg1> [arg2] [arg3] ..."
	exit 1
fi

echo "Number of arguments: $#"

if [ $# -ge 2 ]; then
	echo "The second argument is: $2"
else
	echo "There is no second argument."
fi

