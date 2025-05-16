"""
This module defines Azure Functions for an HTTP-triggered function and a timer-triggered function.
It demonstrates how to handle HTTP requests and execute periodic tasks using Azure Functions.
"""

# Provides logging capabilities to track events and debug the application.
import logging
import azure.functions as func  # Azure Functions Python library.
# Importing the Kraken module from cb0t package.
import cb0t.kraken_api as kraken_api

app = func.FunctionApp()


@app.route(route="ticker", auth_level="anonymous")
def ticker(req: func.HttpRequest) -> func.HttpResponse:
    """
    HTTP triggered function to handle requests for the Kraken ticker.
    It retrieves the ticker information from the Kraken module and returns it as a JSON response.
    """
    logging.info('Ticker function is processing a request.')

    # Extracting the 'pair' parameter from the request.
    pair = req.params.get('pair')
    if not pair:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            pair = req_body.get('pair')

    # If 'pair' is provided, fetch the ticker information.
    if pair:
        logging.info('Pair: %s', pair)
        try:

            t = kraken_api.ticker(pair)

        except kraken_api.KrakenAPIException as e:
            logging.error(str(e))
            return func.HttpResponse(str(e), status_code=500)

        logging.info('Ticker data: %s', t)
        return func.HttpResponse(str(t), mimetype="application/json", status_code=200)

    else:
        return func.HttpResponse("Parameter 'pair' is required.", status_code=400)


@app.timer_trigger(schedule="0 */5 * * * *", arg_name="myTimer", run_on_startup=False,
                   use_monitor=False)
def MyTimerFunction(myTimer: func.TimerRequest) -> None:

    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')
