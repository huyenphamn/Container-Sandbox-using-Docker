#!/bin/bash

echo "Starting memory exhaustion test..."

# Try to allocate more memory than the container's limit (256MB)
stress --vm 1 --vm-bytes 512M --vm-hang 0

# Stress start memory thread and allocate 512MB every thread while we set the memory limit to be 256
# It will sigkill and terminate the process immediately