#!/bin/bash

echo "Monitoring power status changes..."

dbus-monitor --system "type='signal',interface='org.freedesktop.UPower',member='DeviceChanged'" |
while read -r line; do
    if [[ $line == *"power_supply_battery"* ]]; then
        STATUS=$(upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep "state" | awk '{print $2}')

        if [[ $STATUS == "discharging" ]]; then
            echo "This machine is currently using the battery."
        elif [[ $STATUS == "charging" ]] || [[ $STATUS == "fully-charged" ]]; then
            echo "This machine is currently plugged in."
        fi
    fi
done
