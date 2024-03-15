#!/bin/bash
# Title: Run statistics.py for traces with name pattern "IBMObjectStoreTraceXXXPartX" files
# Description: This script runs the statistics.py script for all traces with the name pattern "IBMObjectStoreTrace000Part0" to "IBMObjectStoreTrace097Part9", missing files are skipped.

for i in {11..20}; do
    for j in {0..9}; do
        file="IBMObjectStoreTrace$(printf '%03d' $i)Part$j"
        if [ -f "$file" ]; then
            python3 statistics.py "$file"
        fi
    done
done
