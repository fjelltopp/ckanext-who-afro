import logging
from flask import Blueprint, render_template
import ckan.plugins.toolkit as tk
from typing import Any, cast
from ckan.types import Context, Response
from ckanext.activity.views import (
    _get_activity_stream_limit,
    _get_dashboard_context,
    _extra_template_variables,
    _get_older_activities_url,
    _get_newer_activities_url
)

log = logging.getLogger(__name__)

blueprint = Blueprint(
    "account", __name__, url_prefix="/user"
)


def _get_context():
    return cast(
        Context,
        {
            "auth_user_obj": tk.g.userobj,
            "for_view": True,
        },
    )


def _get_activities_urls(has_more, activity_stream, type=None, name=None, id=None):
    if name is not None and type is not None:
        return (_get_older_activities_url(has_more, activity_stream, type=type, name=name),
                _get_newer_activities_url(has_more, activity_stream, type=type, name=name))
    elif id is not None:
        return (_get_older_activities_url(has_more, activity_stream, id=id),
                _get_newer_activities_url(has_more, activity_stream, id=id))


@blueprint.get("/account", endpoint="index")
def my_account():
    context = _get_context()

    data_dict: dict[str, Any] = {"user_obj": tk.g.userobj}
    extra_vars = _extra_template_variables(context, data_dict)

    filter_type = tk.request.args.get("type", "")
    filter_id = tk.request.args.get("name", "")
    before = tk.request.args.get("before")
    after = tk.request.args.get("after")

    limit = _get_activity_stream_limit()

    activity_stream = tk.h.dashboard_activity_stream(
        tk.g.userobj.id,
        filter_type=filter_type,
        filter_id=filter_id,
        limit=limit + 1,
        before=before,
        after=after
    )
    has_more = len(activity_stream) > limit
    if has_more:
        if after:
            activity_stream.pop(0)
        else:
            activity_stream.pop()

    older_activities_url, newer_activities_url = _get_activities_urls(has_more=has_more,
                                                                      activity_stream=activity_stream, type=filter_type,
                                                                      name=filter_id)
    extra_vars.update({
        "dashboard_activity_stream": activity_stream,
        "newer_activities_url": newer_activities_url,
        "older_activities_url": older_activities_url
    })
    tk.get_action("dashboard_mark_activities_old")(context, {})

    return tk.render("user/account/account_newsfeed.html", extra_vars)


@blueprint.route("/account/activity", endpoint="activity")
def my_account_activity():
    context = _get_context()

    data_dict: dict[str, Any] = {
        "id": tk.g.userobj.id,
        "user_obj": tk.g.userobj,
        "include_num_followers": True,
    }

    extra_vars = _extra_template_variables(context, data_dict)
    before = tk.request.args.get("before")
    after = tk.request.args.get("after")

    limit = _get_activity_stream_limit()

    try:
        activity_stream = tk.get_action(
            "user_activity_list"
        )(context, {
            "id": extra_vars["user_dict"]["id"],
            "before": before,
            "after": after,
            "limit": limit + 1,
        })
    except tk.ValidationError:
        tk.abort(400)

    has_more = len(activity_stream) > limit

    if has_more:
        if after:
            activity_stream.pop(0)
        else:
            activity_stream.pop()

    older_activities_url, newer_activities_url = _get_activities_urls(has_more=has_more,
                                                                      activity_stream=activity_stream,
                                                                      id=id)
    extra_vars.update({
        "id": id,
        "activity_stream": activity_stream,
        "newer_activities_url": newer_activities_url,
        "older_activities_url": older_activities_url
    })

    return tk.render("user/account/account_my_activity.html", extra_vars)
