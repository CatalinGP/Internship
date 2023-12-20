#!/bin/bash


BATTERY_PATH=$(upower -e | grep 'battery') 

while true; do
    STATUS=$(upower -i "$BATTERY_PATH" | grep "state" | awk '{print $2}')

    if [[ $STATUS == "discharging" ]]; then
        echo "This machine is currently using the battery."
    elif [[ $STATUS == "charging" ]] || [[ $STATUS == "fully-charged" ]]; then
        echo "This machine is currently plugged in."
    fi

    sleep 5
done

