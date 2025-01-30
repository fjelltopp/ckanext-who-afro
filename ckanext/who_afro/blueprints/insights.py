import logging

import ckan.plugins.toolkit as tk
from flask import Blueprint, render_template

log = logging.getLogger(__name__)

blueprint = Blueprint(
    "insights", __name__, url_prefix="/insights"
)


@blueprint.get("/", endpoint="index")
def featured_insights():
    return tk.redirect_to("errors.under-construction")
    # return render_template("insights/featured.html")
