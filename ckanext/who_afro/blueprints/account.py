import logging
from flask import Blueprint, render_template

log = logging.getLogger(__name__)

blueprint = Blueprint(
    "account", __name__, url_prefix="/user"
)


@blueprint.get("/account", endpoint="account")
def my_account():
    return render_template("user/account.html")
