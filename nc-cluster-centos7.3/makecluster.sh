#!/bin/bash

GROUP="serpent"
LOCATION="southcentralus"
DNS_NAME="serpent"
MASTER_VM_SIZE="Standard_A8"
WORKER_VM_SIZE="Standard_NC24r"
IMAGE="/subscriptions/4c217c02-7b06-42da-b13c-e8de392fbd00/resourceGroups/petibm-GPU-IntelMPI/providers/Microsoft.Compute/images/petibm-image"
ADMIN_USERNAME=$1
ADMIN_PASSWORD=$2

echo "[INFO] Creating resource group ..."
az group create \
  --name ${GROUP} \
  --location ${LOCATION}

echo "[INFO] Creating public ip ..."
az network public-ip create \
  --resource-group ${GROUP} \
  --name public-ips \
  --dns-name ${DNS_NAME} \
  --location ${LOCATION} \
  --allocation-method Dynamic

echo "[INFO] Creating virtual network and subnet ..."
az network vnet create \
  --resource-group ${GROUP} \
  --name virtualnetwork  \
  --address-prefixes 10.0.0.0/16 \
  --subnet-name subnetwork \
  --subnet-prefix 10.0.0.0/24 \
  --location ${LOCATION}

# Master node
echo "[INFO] Master: Creating network interface ..."
az network nic create \
  --resource-group ${GROUP} \
  --name nic \
  --vnet-name virtualnetwork \
  --subnet subnetwork \
  --private-ip-address 10.0.0.254 \
  --public-ip-address public-ips \
  --location ${LOCATION}

echo "[INFO] Master: Creating virtual machine ..."
az vm create \
  --resource-group ${GROUP} \
  --name master \
  --location ${LOCATION} \
  --size ${MASTER_VM_SIZE} \
  --image ${IMAGE} \
  --admin-username ${ADMIN_USERNAME} \
  --admin-password ${ADMIN_PASSWORD} \
  --authentication-type password \
  --nics nic \
  --os-disk-name osdisk \
  --os-disk-caching ReadWrite \
  --storage-sku Standard_LRS

echo "[INFO] Master: Attaching data disk ..."
az vm disk attach \
  --resource-group ${GROUP} \
  --disk datadisk0 \
  --vm-name master \
  --lun 0 \
  --caching ReadWrite \
  --size-gb 128 \
  --sku Standard_LRS \
  --new

echo "[INFO] Creating availability set ..."
az vm availability-set create \
  --resource-group ${GROUP} \
  --name avset \
  --location ${LOCATION} \
  --platform-fault-domain-count 2 \
  --platform-update-domain-count 2

# Worker0 node
echo "[INFO] Worker0: Creating network interface ..."
az network nic create \
  --resource-group ${GROUP} \
  --name nic-worker0 \
  --vnet-name virtualnetwork \
  --subnet subnetwork \
  --private-ip-address 10.0.0.5 \
  --location ${LOCATION}

echo "[INFO] Worker0: Creating virtual machine ..."
az vm create \
  --resource-group ${GROUP} \
  --name worker0 \
  --location ${LOCATION} \
  --size ${WORKER_VM_SIZE} \
  --image ${IMAGE} \
  --admin-username ${ADMIN_USERNAME} \
  --admin-password ${ADMIN_PASSWORD} \
  --authentication-type password \
  --nics nic-worker0 \
  --availability-set avset \
  --os-disk-name osdisk-worker0 \
  --os-disk-caching ReadWrite \
  --storage-sku Standard_LRS

# Worker1 node
echo "[INFO] Worker1: Creating network interface ..."
az network nic create \
  --resource-group ${GROUP} \
  --name nic-worker1 \
  --vnet-name virtualnetwork \
  --subnet subnetwork \
  --private-ip-address 10.0.0.6 \
  --location ${LOCATION}

echo "[INFO] Worker1: Creating virtual machine ..."
az vm create \
  --resource-group ${GROUP} \
  --name worker1 \
  --location ${LOCATION} \
  --size ${WORKER_VM_SIZE} \
  --image ${IMAGE} \
  --admin-username ${ADMIN_USERNAME} \
  --admin-password ${ADMIN_PASSWORD} \
  --authentication-type password \
  --nics nic-worker1 \
  --availability-set avset \
  --os-disk-name osdisk-worker1 \
  --os-disk-caching ReadWrite \
  --storage-sku Standard_LRS

# Post-installation steps
echo "[INFO] Master: Performing post-installation steps ..."
az vm extension set \
  --resource-group ${GROUP} \
  --vm-name master \
  --publisher Microsoft.Azure.Extensions \
  --version 2.0 \
  --name CustomScript \
  --settings postinstall.json

echo "[INFO] Worker0: Performing post-installation steps ..."
az vm extension set \
  --resource-group ${GROUP} \
  --vm-name worker0 \
  --publisher Microsoft.Azure.Extensions \
  --version 2.0 \
  --name CustomScript \
  --settings postinstall.json

echo "[INFO] Worker1: Performing post-installation steps ..."
az vm extension set \
  --resource-group ${GROUP} \
  --vm-name worker1 \
  --publisher Microsoft.Azure.Extensions \
  --version 2.0 \
  --name CustomScript \
  --settings postinstall.json

echo "[INFO] Done!"
