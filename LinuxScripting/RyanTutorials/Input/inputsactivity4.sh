#!/bin/bash

ls -l | awk '{print "Filename: " $9, "Size: " $5, "Owner: " $3}'
