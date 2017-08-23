# Deploy Azure cluster with NC nodes as workers

Configuration files adapted from [Azure Quickstart Templates](https://github.com/Azure/azure-quickstart-templates).

```
GROUP_NAME=<group-name>
LOCATION=<a-location>

az group create \
    --name $GROUP_NAME \
    --location $LOCATION

az group deployment create \
    --name $GROUP_NAME-deployment \
    --resource-group $GROUP_NAME \
    --parameters azuredeploy.parameters.json \
    --template-file azuredeploy.json
```