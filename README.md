CB0T
====

As small and simple bot to buy cryptoocurrency on Kraken using the Kraken API.

Log
---

Set the Python version to 3.12.10, as it offers the longest support in Azure (until 2028).

To set up the environment, use the following commands:

    pyenv install 3.12.10
    pyenv local 3.12.10

The project was initialized using the Azure Functions CLI with the following command:

    func init --python

Added some test functions to the project using the following command:

    func new --name test --template "HTTP trigger"

started the Azure Functions project using the following command:

    func start

Next is deployment to Azure. The following command will deploy the project to Azure:

    az login
    az group create --name cb0trg --location germanywestcentral
    az storage account create --name cb0tsto --sku Standard_LRS
    az functionapp create --consumption-plan-location germanywestcentral --runtime python --runtime-version 3.12 --functions-version 4 --name cb0t --os-type linux
    func azure functionapp publish cb0t

Delete the function app using the following command:

    az group delete --name cb0t

Activation of the GitHub Actions deployment was done using the following command:

    az functionapp deployment github-actions add --repo "r0nny8000/cb0t" -g cb0trg -n cb0t --login-with-github -b main
