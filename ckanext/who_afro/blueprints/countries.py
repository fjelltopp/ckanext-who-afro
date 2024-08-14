import logging

from flask import Blueprint
from ckan.plugins import toolkit

log = logging.getLogger(__name__)

blueprint = Blueprint(
    "countries", __name__, url_prefix="/countries"
)


@blueprint.get("/", endpoint="index")
def featured_countries():
    return toolkit.render("countries/index.html")


@blueprint.get("/<country_id>")
def country(country_id=None):
    return toolkit.render(
        "countries/country.html",
        {'country': country_id}
    )
