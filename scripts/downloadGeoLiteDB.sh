#!/bin/bash

SYNAPSE_path="/home/enea/SYNAPSE"

if [ -f "${SYNAPSE_path}/data/GeoLite2-City.mmdb" ]; then
    rm -f ${SYNAPSE_path}/data/GeoLite2-City.mmdb
fi

curl -L -o ${SYNAPSE_path}/data/GeoLite2-City.mmdb https://git.io/GeoLite2-City.mmdb