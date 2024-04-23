#!/bin/bash

URL="https://git.io/GeoLite2-City.mmdb"
DEST_FOLDER="/home/user/SYNAPSE/data"

if [ -f "$DEST_FOLDER/GeoLite2-City.mmdb" ]; then
    rm "$DEST_FOLDER/GeoLite2-City.mmdb"
fi

curl -o "$DEST_FOLDER/GeoLite2-City.mmdb" "$URL"

chown -R user: SYNAPSE/