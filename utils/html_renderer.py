"""HTML rendering utilities."""
import os
import json
import azure.functions as func
from jinja2 import Environment, FileSystemLoader

template_dir = os.path.join(os.path.dirname(__file__), "../html/")
jinja_env = Environment(loader=FileSystemLoader(template_dir))


def html(template: str, *args, **kwargs) -> func.HttpResponse:
    """Renders the HTML template with the current environment and schedule."""
    template_obj = jinja_env.get_template(template)
    return func.HttpResponse(
        template_obj.render(*args, **kwargs), mimetype="text/html", status_code=200
    )


def print_json(obj: dict) -> None:
    """Prints a JSON object in a pretty format for debugging purposes."""
    print(json.dumps(obj, indent=4, default=str))
