#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Usage: $0 <name> <age> <favorite_color>"
  exit 1
fi

name="$1"
age="$2"
color="$3"
current_datetime=$(date "+%Y-%m-%d %H:%M:%S")
hostname=$(hostname)

message="Hello, $name! You are $age years old, and your favorite color is $color."
system_info="This script ran on $current_datetime on host $hostname."

echo "$message"
echo "$system_info"
