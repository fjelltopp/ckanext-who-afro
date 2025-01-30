import logging

from flask import Blueprint, render_template

log = logging.getLogger(__name__)

blueprint = Blueprint(
    "errors", __name__, url_prefix="/errors"
)


@blueprint.get("/", endpoint="under-construction")
def under_construction():
    return render_template("under-construction.html")
