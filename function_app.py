"""Main Azure Functions entry point that registers all routes and triggers."""

import os
import azure.functions as func
from routes.index import index
from routes.simulations import get_simulations
from routes.ticker import get_ticker
from routes.balance import get_balance
from timers.accumulate import accumulate_assets

app = func.FunctionApp()

# Register HTTP routes
app.route(route="{*path}", auth_level="anonymous", methods=["GET"])(index)
app.route(route="balance", auth_level="anonymous", methods=["GET"])(get_balance)
app.route(route="ticker", auth_level="anonymous", methods=["GET"])(get_ticker)
app.route(route="simulations", auth_level="anonymous", methods=["GET"])(get_simulations)

# Register timer trigger
env = os.getenv("CB0TENV", "DEV")
env_schedule = {"DEV": "*/20 * * * * *", "PROD": "0 0 16 * * *"}
app.timer_trigger(schedule=env_schedule[env], arg_name="timer", run_on_startup=False, use_monitor=False)(accumulate_assets)
