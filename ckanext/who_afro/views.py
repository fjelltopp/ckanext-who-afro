import ckan.plugins.toolkit as tk
from typing import Any, cast
from ckan.types import Context
from ckanext.activity.views import (
    _get_activity_stream_limit,
    _get_dashboard_context,
    _extra_template_variables,
    _get_older_activities_url,
    _get_newer_activities_url
)


def _get_context():
    return cast(
        Context,
        {
            "auth_user_obj": tk.g.userobj,
            "for_view": True,
        },
    )

def _get_activities_urls(has_more, activity_stream, **kwargs):
    if 'type' in kwargs and 'name' in kwargs:
        args = {'type': kwargs['type'], 'name': kwargs['name']}
    elif 'id' in kwargs:
        args = {'id': kwargs['id']}
    else:
        raise ValueError("Either 'type' and 'name' or 'id' must be provided")

    older_url = _get_older_activities_url(has_more, activity_stream, **args)
    newer_url = _get_newer_activities_url(has_more, activity_stream, **args)

    return (older_url, newer_url)


def get_dashboard_activity_extra_vars():
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

    return extra_vars


def get_user_activity_extra_vars():
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

    return extra_vars
