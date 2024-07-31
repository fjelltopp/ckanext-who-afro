import logging

from flask import Blueprint, render_template

log = logging.getLogger(__name__)

blueprint = Blueprint(
    "sources", __name__, url_prefix="/sources"
)


@blueprint.get("/", endpoint="index")
def sources_list():
    return render_template("sources/index.html")
