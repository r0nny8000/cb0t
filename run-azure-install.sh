#!/bin/bash
# This script is used to create an Azure Function App and publish the function to it.
az login
az group create --name cb0trg --location germanywestcentral
az storage account create --name cb0tsto --sku Standard_LRS
az functionapp create --consumption-plan-location germanywestcentral --runtime python --runtime-version 3.12 --functions-version 4 --name cb0t --os-type linux
sleep 10
func azure functionapp publish cb0t