import logging

from flask import Blueprint, render_template
from ckanext.activity.views import dashboard

log = logging.getLogger(__name__)

blueprint = Blueprint(
    "userflow", __name__, url_prefix="/dashboard"
)


@blueprint.get("/", endpoint="index")
def dashboard_index():
    return dashboard()
