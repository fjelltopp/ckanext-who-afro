import logging

from flask import Blueprint, render_template
from ckanext.activity.views import dashboard

log = logging.getLogger(__name__)

blueprint = Blueprint(
    "dashboard_extension", __name__, url_prefix="/dashboard"
)


# Returns dashboard but with a different request.path
@blueprint.get("/user_activity", endpoint="user_activity")
def dashboard_index():
    return dashboard()
