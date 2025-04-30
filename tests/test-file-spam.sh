#!/bin/bash
echo "This is file spam. Ultimately should test the read-only and memory exhaustion protection!"

TARGET_DIR="/tmp/spam"

mkdir -p "$TARGET_DIR"

# Create 10,000 small files
for i in $(seq 1 10000); do
  echo "This is spam file $i" > "$TARGET_DIR/file_$i.txt"
done

echo "File spam attack finished."

#This should print out something like "No such file or directory" as container stop from creating spam files.
