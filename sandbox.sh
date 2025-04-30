#!/bin/bash

SCRIPT=$1
TIMEOUT_SECONDS=15 

if [ ! -f "$SCRIPT" ]; then
    echo "Error: Script $SCRIPT not found!"
    exit 1
fi

START_TIME=$(date +%s)

# Record start time when the Docker container begins
docker run --rm -it \
  --read-only \
  --cpus="0.5" \
  --memory="256m" \
  --pids-limit 100 \
  -v "$(pwd)/$SCRIPT":/sandbox/untrusted.sh:ro \
  minimal-sandbox \
  timeout ${TIMEOUT_SECONDS}s bash /sandbox/untrusted.sh \

# Record end time after the Docker container finishes
END_TIME=$(date +%s)

# Calculate and log the execution time
echo "Test: $SCRIPT" >> timeout_log.txt
echo "Execution Time: $(($END_TIME - $START_TIME)) seconds" >> timeout_log.txt
