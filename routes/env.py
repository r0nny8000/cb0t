"""Environment-related HTTP routes."""
import os
import azure.functions as func
from utils.html_renderer import html


def get_env(req: func.HttpRequest) -> func.HttpResponse:
    """Fetches and returns the environment variables."""
    env = os.getenv("CB0TENV", "DEV")
    return html("env.html.j2", env=env)
