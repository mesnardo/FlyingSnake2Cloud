# Create a VM image


On the VM:
```
sudo waagent -deprovision+user
```

Exit the VM and:
```
az vm deallocate \
  --resource-group <group-name> \
  --name <vm-name>

az vm generalize \
  --resource-group <group-name> \
  --name <vm-name>

az image create \
  --resource-group <group-name> \
  --name <image-name> \
  --source <vm-name>
```

We can now create a VM from the captured image.

