import logging

from flask import Blueprint, render_template

log = logging.getLogger(__name__)

blueprint = Blueprint(
    "countries", __name__, url_prefix="/countries"
)


@blueprint.get("/", endpoint="index")
def featured_countries():
    return render_template("countries/index.html")
