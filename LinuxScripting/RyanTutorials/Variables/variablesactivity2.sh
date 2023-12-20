#!/bin/bash

# Define the path to the word list file
word_list="/usr/share/dict/words"

# Check if the word list file exists
if [ -f "$word_list" ]; then
	random_word=$(shuf -n 1 "$word_list")
	echo "Random word: $random_word"
else
	echo "Word list file not found: $word_list"
	exit 1
fi

