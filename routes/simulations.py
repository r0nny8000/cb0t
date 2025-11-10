"""Environment-related HTTP routes."""

import os
import azure.functions as func
from utils.html_renderer import html


def get_simulations(req: func.HttpRequest) -> func.HttpResponse:
    """"""

    return html("simulations.html.j2", env=None)
