#!/bin/bash

# Check if at least one argument is provided
if [ $# -eq 0 ]; then
	echo "Usage: $0 <word_length> [arg1] [arg2] [arg3] ..."
	exit 1
fi


if [[ "$1" =~ ^[0-9]+$ ]]; then
	word_length="$1"
	shift # Remove the first argument from the list
else
	word_length=0
fi

num_arguments=$#
echo "Number of arguments: $num_arguments"

if [ $# -ge 2 ]; then
	echo "The second argument is: $2"
else
	echo "There is no second argument."
fi

# Use grep to filter words if a word lengh filter is specified
if [ "$word_length" -gt 0 ]; then
	filtered_words=$(grep -E "^.{$word_length}$" <<< "$@")
	if [ -n "$filtered_words" ]; then
		echo "Words with $word_length characters:"
		echo "$filtered_words"
	else
		echo "No words with $word_length characters found."
	fi
fi

