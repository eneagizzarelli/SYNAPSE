#!/bin/bash

SYNAPSE_path="/home/enea/SYNAPSE"

if [ -d "${SYNAPSE_path}" ]; then
    sudo rm -rf ${SYNAPSE_path}
fi

git clone https://github.com/eneagizzarelli/SYNAPSE.git ${SYNAPSE_path}

mkdir -p ${SYNAPSE_path}/logs
mkdir -p ${SYNAPSE_path}/data

python ${SYNAPSE_path}/scripts/downloadGeoLiteDB.py

sudo chown -R enea:enea ${SYNAPSE_path}
sudo chmod -R 700 ${SYNAPSE_path}