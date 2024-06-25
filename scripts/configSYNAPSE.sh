#!/bin/bash

#
# Convenience script to configure SYNAPSE.
# Mainly used to update the local configuration after the code has been modified.
#   1. Previous SYNAPSE folder is removed and the new one is cloned in the same location.
#   2. "logs" and "data" folders are created.
#   3. GeoLite2-City.mmdb is downloaded leveraging downloadGeoLiteDB.sh script.
#   4. Ownership and permissions are set to the enea user.
# This script must be executed as root.
#

SYNAPSE_path="/home/enea/SYNAPSE"

if [ -d "${SYNAPSE_path}" ]; then
    sudo rm -rf ${SYNAPSE_path}
fi

git clone https://github.com/eneagizzarelli/SYNAPSE.git ${SYNAPSE_path}

mkdir -p ${SYNAPSE_path}/logs
mkdir -p ${SYNAPSE_path}/data

${SYNAPSE_path}/scripts/downloadGeoLiteDB.sh

sudo chown -R enea:enea ${SYNAPSE_path}
sudo chmod -R 700 ${SYNAPSE_path}