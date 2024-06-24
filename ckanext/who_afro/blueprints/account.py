import logging
import ckan.plugins.toolkit as tk
from flask import Blueprint, render_template
import ckanext.who_afro.views as views

log = logging.getLogger(__name__)

blueprint = Blueprint(
    "account", __name__, url_prefix="/user"
)


@blueprint.get("/account", endpoint="index")
def my_account_newsfeed():
    return tk.render("user/account/account_newsfeed.html", views.get_dashboard_activity_extra_vars())


@blueprint.route("/account/activity", endpoint="activity")
def my_account_activity():
    return tk.render("user/account/account_my_activity.html", views.get_user_activity_extra_vars())
