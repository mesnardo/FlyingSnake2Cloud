#!/bin/bash
# Deploy cluster on Azure using Azure-cli

# create a resource group
az group create \
  --location eastus \
  --name snakea9-rg

# deploy resources
CONFIG_FILE="azuredeploy.json"
az group deployment create \
  --resource-group snakea9-rg \
  --name snakea9-deploy \
  --template-file ${CONFIG_FILE}

