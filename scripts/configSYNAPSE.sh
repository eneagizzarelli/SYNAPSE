#!/bin/bash

SYNAPSE_path="/home/enea/SYNAPSE"

if [ -d "${SYNAPSE_path}" ]; then
    rm -rf ${SYNAPSE_path}
fi

git clone https://github.com/eneagizzarelli/SYNAPSE.git ${SYNAPSE_path}

mkdir -p ${SYNAPSE_path}/logs
mkdir -p ${SYNAPSE_path}/data

curl -L -o ${SYNAPSE_path}/data/GeoLite2-City.mmdb https://git.io/GeoLite2-City.mmdb

sudo chown -R enea:enea ${SYNAPSE_path}
sudo chmod -R 700 ${SYNAPSE_path}