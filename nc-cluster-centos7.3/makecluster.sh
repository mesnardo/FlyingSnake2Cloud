#!/bin/bash

GROUP="serpent"
LOCATION="southcentralus"
DNS_NAME="serpent"
MASTER_VM_SIZE="Standard_A8"
WORKER_VM_SIZE="Standard_NC24r"
IMAGE="/subscriptions/4c217c02-7b06-42da-b13c-e8de392fbd00/resourceGroups/snakenc24-test/providers/Microsoft.Compute/images/snake-image"

az group create \
  --name ${GROUP} \
  --location ${LOCATION} \
  --debug

az storage account create \
  --resource-group ${GROUP} \
  --name ${GROUP}2storage \
  --location ${LOCATION} \
  --sku Standard_LRS \
  --kind storage

az network public-ip create \
  --resource-group ${GROUP} \
  --name public-ips \
  --dns-name ${DNS_NAME} \
  --location ${LOCATION} \
  --allocation-method Dynamic \
  --debug

az network vnet create \
  --resource-group ${GROUP} \
  --name virtualnetwork  \
  --address-prefixes 10.0.0.0/16 \
  --subnet-name subnetwork \
  --subnet-prefix 10.0.0.0/24 \
  --location ${LOCATION} \
  --debug


# Master node
az network nic create \
  --resource-group ${GROUP} \
  --name nic \
  --vnet-name virtualnetwork \
  --subnet subnetwork \
  --private-ip-address 10.0.0.254 \
  --public-ip-address public-ips \
  --location ${LOCATION}
  --debug

az vm create \
  --resource-group ${GROUP} \
  --name master \
  --location ${LOCATION} \
  --size ${MASTER_VM_SIZE} \
  --image ${IMAGE} \
  --admin-username mesnardo \
  --admin-password "$FlyingSnake24" \
  --authentication-type password \
  --nics nic \
  --storage-sku Standard_LRS \
  --debug

az vm unmanaged-disk attach \
  --resource-group ${GROUP} \
  --name datadisk0 \
  --vm-name master \
  --lun 0 \
  --size-gb 10 \
  --caching ReadWrite \
  --vhd-uri "http://"${GROUP}"2storage.blob.core.windows.net/vhds/master-datadisk0.vhd" \
  --new \
  --debug

# Worker0 node
az network nic create \
  --resource-group ${GROUP} \
  --name nic-worker0 \
  --vnet-name virtualnetwork \
  --subnet subnetwork \
  --debug

az vm create \
  --resource-group ${GROUP} \
  --name worker0 \
  --location ${LOCATION} \
  --size ${VM_SIZE} \
  --image ${IMAGE} \
  --admin-username mesnardo \
  --admin-password "$FlyingSnake24" \
  --authentication-type password \
  --nics nic-worker0 \
  --storage-sku Standard_LRS \
  --debug