#!/bin/bash

echo -n "Enter your name: "
read name

echo -n "Enter your age: "
read age

echo -n "Enter your favorite color: "
read color

message="Hello, $name! You are $age years old, and your favorite color is $color."

echo "$message"
