#!/bin/bash
# Stopt and deallocate the Azure cluster using Azure-cli

# parameters
RESOURCE_GROUP="snakea9-rg"
MASTER_NAME="master"
WORKER_PREFIX="worker"
MIN_INDEX_WORKER=0
MAX_INDEX_WORKER=7

# stop and deallocate workers
for i in `seq ${MIN_INDEX_WORKER} ${MAX_INDEX_WORKER}`
do
  az vm deallocate --resource-group ${RESOURCE_GROUP} --name ${WORKER_PREFIX}$i
done

# stop and deallocate master
az vm deallocate --resource-group ${RESOURCE_GROUP} --name ${MASTER_NAME}

