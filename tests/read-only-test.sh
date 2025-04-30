#!/bin/bash

echo "Testing read-only, this should not work!"

# Try to create or modify a file 
echo "Attempting to write to a file..."
echo "This is a test" > /sandbox/testfile.txt

