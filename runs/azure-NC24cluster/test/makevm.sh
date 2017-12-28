#!/bin/bash

GROUP="test"
LOCATION="southcentralus"
DNS_NAME="mesnardotest"
VM_SIZE="Standard_NC24r"
IMAGE="OpenLogic:CentOS-HPC:7.3:7.3.20170606"
ADMIN_USERNAME=$1
PASSWORD=$2

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

echo "[INFO] Creating network interface ..."
az network nic create \
  --resource-group ${GROUP} \
  --name nic \
  --vnet-name virtualnetwork \
  --subnet subnetwork \
  --private-ip-address 10.0.0.5 \
  --public-ip-address public-ips \
  --location ${LOCATION}

echo "[INFO] Creating virtual machine ..."
az vm create \
  --resource-group ${GROUP} \
  --name master \
  --location ${LOCATION} \
  --size ${VM_SIZE} \
  --image ${IMAGE} \
  --admin-username ${ADMIN_USERNAME} \
  --admin-password ${PASSWORD} \
  --authentication-type password \
  --nics nic \
  --os-disk-name osdisk \
  --os-disk-caching ReadWrite \
  --storage-sku Standard_LRS

echo "[INFO] Done!"
