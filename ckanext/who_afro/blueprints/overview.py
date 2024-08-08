import logging
from ckan.plugins import toolkit
from flask import Blueprint

log = logging.getLogger(__name__)

blueprint = Blueprint(
    "overview", __name__, url_prefix="/overview"
)


@blueprint.get("/<dataset_id>")
def overview(dataset_id=None):
    data_dict = {'id': dataset_id, 'include_tracking': True}
    try:
        pkg_dict = toolkit.get_action('package_show')({}, data_dict)
    except (toolkit.ObjectNotFound, toolkit.NotAuthorized):
        return toolkit.abort(
            404,
            toolkit._('Dataset not found or you have no permission to view it')
        )

    if not toolkit.h.dataset_has_overview(pkg_dict):
        return toolkit.abort(
            404,
            toolkit._('Dataset does not have overview')
        )
    return toolkit.render(
            'package/overview.html', {
                'dataset_type': pkg_dict['type'],
                'pkg_dict': pkg_dict,
                'pkg': pkg_dict,
            }
        )
