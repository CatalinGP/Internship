#!/bin/bash

current_day=$(date +%u)

case $current_day in
	1)
		echo "Happy Sunday!"
		;;
	2)
		echo "Hello Monday!"
		;;
	3)
		echo "Happy Tuesday!"
		;;
	4)
		echo "Happy Hump Day (Wednesday)!"
		;;
	5)
		echo "TGIF (Friday)!"
		;;
	6)
		echo "Happy Saturday!"
		;;
	7)
		echo "Happy Sunday!"
		;;
	*)
		echo "Enjoy your day!"
		;;
esac
