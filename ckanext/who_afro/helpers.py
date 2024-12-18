import logging
import ckan.model as model
from ckan.common import request, g
from datetime import datetime, timedelta
from ckan.plugins import toolkit

log = logging.getLogger(__name__)


def get_user_obj(field=""):
    """
    Returns an attribute of the user object, or returns the whole user object.
    """
    return getattr(g.userobj, field, g.userobj)


def get_dataset_from_id(id, validate=False):
    context = {
        "model": model,
        "ignore_auth": True,
        "validate": validate,
        "use_cache": False,
    }
    package_show_action = toolkit.get_action("package_show")
    return package_show_action(context, {"id": id})


def get_facet_items_dict(facet, search_facets=None, limit=None, exclude_active=False):
    """
    Overwrite of core CKAN helper in order to get custom sorting order
    on some of the facets.

    Arguments:
    facet -- the name of the facet to filter.
    search_facets -- dict with search facets(c.search_facets in Pylons)
    limit -- the max. number of facet items to return.
    exclude_active -- only return unselected facets.

    """
    if (
        not search_facets
        or not isinstance(search_facets, dict)
        or not search_facets.get(facet, {}).get("items")
    ):
        return []

    facets = []

    for facet_item in search_facets[facet]["items"]:
        if not len(facet_item["name"].strip()):
            continue

        params_items = request.params.items(multi=True)

        if not (facet, facet_item["name"]) in params_items:
            facets.append(dict(active=False, **facet_item))
        elif not exclude_active:
            facets.append(dict(active=True, **facet_item))

    # Replace CKAN default sort method
    facets = _facet_sort_function(facet, facets)
    if hasattr(g, "search_facets_limits"):
        if g.search_facets_limits and limit is None:
            limit = g.search_facets_limits.get(facet)

    # Zero treated as infinite for hysterical raisins
    if limit is not None and limit > 0:
        return facets[:limit]

    return facets


def _facet_sort_function(facet_name, facet_items):

    if facet_name == "year":
        # Custom sort of year facet
        facet_items.sort(key=lambda it: it["display_name"].lower(), reverse=True)
    else:
        # Default CKAN sort
        # Descendingly by count and ascendingly by case-sensitive display name
        facet_items.sort(key=lambda it: (-it["count"], it["display_name"].lower()))

    return facet_items


def get_all_groups():
    return toolkit.get_action("group_list")(
        data_dict={"sort": "title asc", "all_fields": True}
    )


def get_featured_datasets():
    featured_datasets = toolkit.get_action("package_search")(
        data_dict={"fq": "tags:Featured", "sort": "metadata_modified desc", "rows": 3}
    )["results"]
    recently_updated = toolkit.get_action("package_search")(
        data_dict={"q": "*:*", "sort": "metadata_modified desc", "rows": 3}
    )["results"]
    datasets = featured_datasets + recently_updated
    return datasets[:3]


def get_user_from_id(userid):
    user_show_action = toolkit.get_action("user_show")
    user_info = user_show_action({}, {"id": userid})
    return user_info["fullname"]


def comma_swap_formatter(input):
    """
    Swaps the parts of a string around a single comma.
    Use to format e.g. "Tanzania, Republic of" as "Republic of Tanzania"
    """
    if input.count(",") == 1:
        parts = input.split(",")
        stripped_parts = list(map(lambda x: x.strip(), parts))
        reversed_parts = reversed(stripped_parts)
        joined_parts = " ".join(reversed_parts)
        return joined_parts
    else:
        return input


def lower_formatter(input):
    return input.lower()


def month_formatter(month):
    return datetime.strptime(month, "%Y-%m").strftime("%b %Y")


def get_recently_updated_datasets():
    recently_updated = toolkit.get_action("package_search")(
        data_dict={"q": "*:*", "sort": "metadata_modified desc", "rows": 3}
    )["results"]
    return recently_updated[:3]


def get_last_modifier(package_id):
    package_activity = toolkit.get_action("package_activity_list")(
        data_dict={"id": package_id}
    )
    return get_user_from_id(package_activity[0]["user_id"])


def format_locale(locale):
    locale_name = (
        locale.display_name if locale.display_name is not None else locale.english_name
    )
    locale_name = locale_name.replace(" (Portugal)", "").capitalize()
    locale_name = locale_name.replace(" (united kingdom)", "").capitalize()
    return locale_name


def get_datahub_stats():
    stats = toolkit.h.get_site_statistics()

    now = datetime.now()
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week_as_str = start_of_week.strftime("%Y-%m-%dT%H:%M:%SZ")

    data_dict = {
        "q": "*:*",
        "fq": "state:active AND metadata_modified:[{} TO NOW]".format(
            start_of_week_as_str
        ),
        "rows": 0,
    }

    result = toolkit.get_action("package_search")({}, data_dict)
    stats["active_datasets_updated_for_current_week"] = result.get("count", 0)

    stats["active_users"] = 0
    users_list = toolkit.get_action("user_list")({})
    active_users = len([user for user in users_list if user["state"] == "active"])
    stats["active_users"] = active_users

    data_dict = {"rows": 0, "facet": "true", "facet.field": ["programme", "country"]}

    stats["programmes"] = 0
    stats["countries"] = 0
    result = toolkit.get_action("package_search")({}, data_dict)
    if "facets" in result:
        if "programme" in result["facets"]:
            stats["programmes"] = len(result["facets"]["programme"])
        if "country" in result["facets"]:
            stats["countries"] = len(result["facets"]["country"])

    return stats


def get_activity_stream_limit():
    base_limit = toolkit.config.get("ckan.activity_list_limit")
    max_limit = toolkit.config.get("ckan.activity_list_limit_max")
    return min(base_limit, max_limit)


def get_license(license_id):
    license_list = toolkit.get_action("license_list")({}, {})
    for license in license_list:
        if license["id"] == license_id:
            return license
    else:
        return {}


def dataset_has_overview(pkg_dict):
    return pkg_dict.get("type", "") in ["indicator"]


def get_indicator_value_field(datastore_info, resource_id):
    value_field = ""

    for field in datastore_info.get("fields", []):
        if field["id"] == "NumericValue":
            value_field = field["id"]
            break
        elif field["id"].endswith("_N") and field["type"] == "numeric":
            value_field = field["id"]
            break
    if not value_field:
        log.warning("No indicator value found for resource %s" % resource_id)

    return value_field


def get_indicator_time_field(datastore_info, resource_id):
    time_field = ""

    for field in datastore_info.get("fields", []):
        if field["id"] == "TimeDim" and field["type"] == "numeric":
            time_field = field["id"]
            break
        elif field["id"] == "DIM_TIME" and field["type"] == "numeric":
            time_field = field["id"]
            break
    if not time_field:
        log.warning("No time values found for resource %s" % resource_id)

    return time_field


def get_indicator_geo_field(datastore_info, resource_id):
    geo_field = ""

    # TODO replace with match when we upgrade to Python 3.10 or higher
    for field in datastore_info.get("fields", []):
        if field["id"] == "SpatialDimLong":
            geo_field = field["id"]
            break
        elif field["id"] == "GEO_NAME_LONG":
            geo_field = field["id"]
            break
        elif field["id"] == "SpatialDim":
            geo_field = field["id"]
            break
        elif field["id"] == "GEO_NAME_SHORT":
            geo_field = field["id"]
            break
    if not geo_field:
        log.warning("No geo field found for resource %s" % resource_id)

    return geo_field


def get_indicator_facet_field(datastore_info, resource_id):
    facet_field = ""
    facet_label = ""

    for field in datastore_info.get("fields", []):
        if field["id"].endswith("DIM_SEX") and field["type"] == "text":
            facet_field = "DIM_SEX"
            facet_label = "Sex"
    if not facet_field:
        log.warning("No facet field found for resource %s" % resource_id)

    return facet_field, facet_label


def get_indicator_details(resource_id):
    datastore_info = {}
    try:
        datastore_info = toolkit.get_action("datastore_info")({}, {"id": resource_id})
    except toolkit.ObjectNotFound:
        log.warning("No datastore found for resource %s" % resource_id)

    value_field = get_indicator_value_field(datastore_info, resource_id)
    time_field = get_indicator_time_field(datastore_info, resource_id)
    geo_field = get_indicator_geo_field(datastore_info, resource_id)
    facet_field, facet_label = get_indicator_facet_field(datastore_info, resource_id)

    return {
        "facet_label": facet_label,
        "facet_field": facet_field,
        "value_field": value_field,
        "geo_field": geo_field,
        "time_field": time_field,
    }
