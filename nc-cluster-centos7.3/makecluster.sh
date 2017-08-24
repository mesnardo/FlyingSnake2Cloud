#!/bin/bash

GROUP="serpent"
LOCATION="southcentralus"
DNS_NAME="serpent"
MASTER_VM_SIZE="Standard_A8"
WORKER_VM_SIZE="Standard_NC24r"
IMAGE="/subscriptions/4c217c02-7b06-42da-b13c-e8de392fbd00/resourceGroups/snakenc24-test/providers/Microsoft.Compute/images/snake-image"

az group create \
  --name ${GROUP} \
  --location ${LOCATION}

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
  --allocation-method Dynamic

az network vnet create \
  --resource-group ${GROUP} \
  --name virtualnetwork  \
  --address-prefixes 10.0.0.0/16 \
  --subnet-name subnetwork \
  --subnet-prefix 10.0.0.0/24 \
  --location ${LOCATION}

# Master node
az network nic create \
  --resource-group ${GROUP} \
  --name nic \
  --vnet-name virtualnetwork \
  --subnet subnetwork \
  --private-ip-address 10.0.0.254 \
  --public-ip-address public-ips \
  --location ${LOCATION}

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
  --os-disk-name osdisk \
  --os-disk-caching ReadWrite \
  --storage-sku Standard_LRS

az vm disk attach \
  --resource-group ${GROUP} \
  --disk datadisk0 \
  --vm-name master \
  --lun 0 \
  --caching ReadWrite \
  --size-gb 128 \
  --sku Standard_LRS \
  --new

az vm extension set \
  --resource-group ${GROUP} \
  --vm-name master \
  --publisher Microsoft.Azure.Extensions \
  --version 2.0 \
  --name CustomScript \
  --settings postinstall.json

# Worker0 node
az network nic create \
  --resource-group ${GROUP} \
  --name nic-worker0 \
  --vnet-name virtualnetwork \
  --subnet subnetwork \
  --private-ip-address 10.0.0.5 \
  --location ${LOCATION}

az vm create \
  --resource-group ${GROUP} \
  --name worker0 \
  --location ${LOCATION} \
  --size ${WORKER_VM_SIZE} \
  --image ${IMAGE} \
  --admin-username mesnardo \
  --admin-password "$FlyingSnake24" \
  --authentication-type password \
  --nics nic-worker0 \
  --os-disk-name osdisk-worker0 \
  --os-disk-caching ReadWrite \
  --storage-sku Standard_LRS

az vm extension set \
  --resource-group ${GROUP} \
  --vm-name worker0 \
  --publisher Microsoft.Azure.Extensions \
  --version 2.0 \
  --name CustomScript \
  --settings postinstall.json

# Worker1 node
az network nic create \
  --resource-group ${GROUP} \
  --name nic-worker1 \
  --vnet-name virtualnetwork \
  --subnet subnetwork \
  --private-ip-address 10.0.0.6 \
  --location ${LOCATION}

az vm create \
  --resource-group ${GROUP} \
  --name worker1 \
  --location ${LOCATION} \
  --size ${WORKER_VM_SIZE} \
  --image ${IMAGE} \
  --admin-username mesnardo \
  --admin-password "$FlyingSnake24" \
  --authentication-type password \
  --nics nic-worker1 \
  --os-disk-name osdisk-worker1 \
  --os-disk-caching ReadWrite \
  --storage-sku Standard_LRS

az vm extension set \
  --resource-group ${GROUP} \
  --vm-name worker1 \
  --publisher Microsoft.Azure.Extensions \
  --version 2.0 \
  --name CustomScript \
  --settings postinstall.json
