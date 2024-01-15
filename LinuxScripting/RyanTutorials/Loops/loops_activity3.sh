#!/bin/bash

code=""
for i in {1..4}; do
	code="${code}$((RANDOM %6 + 1))"
done

echo "Welcome to the masterming game!"
echo "Guess the 4-digit code. each digit is between 1 and 6."
echo "Enter your guess:"

attempts=0

while true; do
	read -r guess
	attempts=$((attempts + 1))

	if [[ ! "$guess" =~ ^[1-6]{4}$ ]]; then
		echo "Wrong guess. Input 4-digit code between 1 and 6"
		continue
	fi

	if [ "$guess" == "$code" ]; then
		echo "You guessed the code: $code"
		echo "You made $attempts attempts."
		break
	else
		correct_digits=0
		for ((i = 0; i < 4; i++)); do
			if [ "${guess:$i:1}" == "${code:$i:1}" ]; then
				correct_digits=$((correct_digits + 1))
			fi
		done

		echo "Incorrect guess. You have $correct_digits correct digits in the right position."


	fi
done
