"""Index route handler."""

import azure.functions as func
from utils.html_renderer import html


def index(req: func.HttpRequest) -> func.HttpResponse:
    """Renders the main index page."""
    return html(template="index.html.j2", headers=req.method)
