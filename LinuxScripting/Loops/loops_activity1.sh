#!/bin/bash

for number in {1..10}; do
	if ((number % 2 == 0)); then
		echo "$number is even"
	else
		echo "$number is odd"
	fi
done
