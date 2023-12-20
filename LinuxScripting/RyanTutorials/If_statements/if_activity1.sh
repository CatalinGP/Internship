#!/bin/bash

if [ $# -ne 2 ]; then
	echo "Usage: $0 <number1> <number2>"
	exit 1
fi

number1="$1"
number2="$2"

if [ "$number1" -gt "$number2" ]; then
	echo "The larger number is: $number1"
elif [ "$number2" -gt "$number1" ]; then
	echo "The larger number is: $number2"
else
	echo "Both numbers are equal: $number1"
fi
