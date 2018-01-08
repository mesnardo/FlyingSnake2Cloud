#!/bin/bash
# Start the Azure cluster using Azure-cli

# parameters
RESOURCE_GROUP="snakea9-rg"
MASTER_NAME="master"
WORKER_PREFIX="worker"
MIN_INDEX_WORKER=0
MAX_INDEX_WORKER=7

# start master
az vm start --resource-group ${RESOURCE_GROUP} --name ${MASTER_NAME}

# start workers
for i in `seq ${MIN_INDEX_WORKER} ${MAX_INDEX_WORKER}`
do
  az vm start --resource-group ${RESOURCE_GROUP} --name ${WORKER_PREFIX}$i
done

