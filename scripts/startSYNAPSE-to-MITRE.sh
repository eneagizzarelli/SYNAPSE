#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 <ip>"
    exit 1
fi

python3 /home/user/SYNAPSE/SYNAPSE-to-MITRE/SYNAPSE-to-MITRE.py "$1"