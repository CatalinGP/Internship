#!/bin/bash

if [ $# -ne 2 ]; then
	echo "Usage: $0 <number1> <number2>"
	exit 1
fi

result=$(( $1 * $2 ))
echo "Result: $result"
