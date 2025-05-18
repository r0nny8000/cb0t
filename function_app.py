"""
This module defines Azure Functions for an HTTP-triggered function and a timer-triggered function.
It demonstrates how to handle HTTP requests and execute periodic tasks using Azure Functions.
"""

# Provides logging capabilities to track events and debug the application.
import logging
import azure.functions as func  # Azure Functions Python library.

# Jinja2 template engine for rendering HTML.
from jinja2 import Environment, FileSystemLoader
from kraken.spot import Market
from kraken.exceptions import *  # pylint: disable=wildcard-import,unused-wildcard-import

import os

app = func.FunctionApp()

# Set up the Jinja2 environment once, at the module level
template_dir = os.path.join(os.path.dirname(__file__), "cb0t/html/")
jinja_env = Environment(loader=FileSystemLoader(template_dir))


@app.route(route="ticker", auth_level="anonymous", )
def get_ticker(req: func.HttpRequest) -> func.HttpResponse:
    """
    HTTP triggered function to handle requests for the Kraken ticker.
    It retrieves the ticker information from the Kraken module and returns it as a JSON response.
    """

    # Extracting the 'pair' parameter from the request.
    pair = req.params.get('pair')

    if not pair:
        return func.HttpResponse("Parameter 'pair' is required.", status_code=400)

    # If 'pair' is provided, fetch the ticker information.
    logging.info("Ticker function is processing with pair: %s", pair)

    try:

        ticker = Market().get_ticker(pair)
        assets = Market().get_asset_pairs(pair)
        logging.info('Ticker data: %s', ticker)

    except (KrakenUnknownAssetError, KrakenUnknownAssetPairError) as e:
        logging.error(str(e))
        return func.HttpResponse(str(e), status_code=500)

    # Render the HTML template with the ticker data.
    template = jinja_env.get_template("ticker.html")
    html = template.render(pair=pair, ticker=ticker, assets=assets)

    return func.HttpResponse(html, mimetype="text/html", status_code=200)


@app.timer_trigger(schedule="0 */5 * * * *", arg_name="accumulator", run_on_startup=False,
                   use_monitor=False)
def accumulator_bot(accumulator: func.TimerRequest) -> None:
    """accumulate crypto"""

    if accumulator.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')
