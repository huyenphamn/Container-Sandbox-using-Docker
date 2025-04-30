#!/bin/bash

echo "This is an infinite loop."
# Infinite loop to burn CPU
# This should only affect the Docker, and terminate after some time (I set the timer for 15 seconds)
while : ; do : ; done
