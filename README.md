CBOT
====

As small and simple bot to buy cryptoocurrency on Kraken using the Kraken API.

Log
---

Set the Python version to 3.12.8, as it offers the longest support in Azure (until 2028).

To set up the environment, use the following commands:

    pyenv install 3.12.8
    pyenv local 3.12.8

The project was initialized using the Azure Functions CLI with the following command:

    func init --python

Added some test functions to the project using the following command:

    func new --name test --template "HTTP trigger"

started the Azure Functions project using the following command:

    func start

Next is deployment to Azure. The following command will deploy the project to Azure:

    az login
    az group create --name cbot-rg --location germanywestcentral
    az storage account create --name cbotstorage --sku Standard_LRS
