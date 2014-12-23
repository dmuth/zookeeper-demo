#!/bin/bash
#
# This script kills all current "create" processes
#

echo "$0: Stopping all create processes..."
pkill -f create-start.sh
pkill -f create.py
echo "Done!"


