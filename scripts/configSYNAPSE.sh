#!/bin/bash

sudo rm -R SYNAPSE/

git clone https://github.com/eneagizzarelli/SYNAPSE.git

mkdir SYNAPSE/logs
mkdir SYNAPSE/data

URL="https://git.io/GeoLite2-City.mmdb"
DEST_FOLDER="/home/user/SYNAPSE/data"
curl -o "$DEST_FOLDER/GeoLite2-City.mmdb" "$URL"

chown -R user: SYNAPSE/