#!/bin/bash

echo "This fork bomb should crash your computer!"
:(){ :|:& };:
sleep 30 # Because the sandbox-container works, it might not be very visible so this line is to compare between the CPU usage 

# This should not crash the computer, and instead of affecting the machine CPU, it only affecting the Docker. 