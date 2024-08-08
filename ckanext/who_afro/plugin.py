import logging
import json
from collections import OrderedDict
from typing import Dict
import ckanext.blob_storage.helpers as blobstorage_helpers
import ckan.lib.uploader as uploader
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.who_afro.actions as who_afro_actions
import ckanext.who_afro.upload as who_afro_upload
import ckanext.who_afro.validators as who_afro_validators
import ckanext.who_afro.helpers as who_afro_helpers
import ckanext.who_afro.blueprints as who_afro_blueprints
from ckan.lib.plugins import DefaultTranslation

log = logging.getLogger(__name__)


class WHOAFROPlugin(plugins.SingletonPlugin, DefaultTranslation):

    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IResourceController, inherit=True)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IBlueprint)

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'max_resource_size': uploader.get_max_resource_size,
            'get_dataset_from_id': who_afro_helpers.get_dataset_from_id,
            'blob_storage_resource_filename': blobstorage_helpers.resource_filename,
            'get_facet_items_dict': who_afro_helpers.get_facet_items_dict,
            'get_all_groups': who_afro_helpers.get_all_groups,
            'get_featured_datasets': who_afro_helpers.get_featured_datasets,
            'get_user_from_id': who_afro_helpers.get_user_from_id,
            'get_user_obj': who_afro_helpers.get_user_obj,
            'month_formatter': who_afro_helpers.month_formatter,
            'get_recently_updated_datasets': who_afro_helpers.get_recently_updated_datasets,
            'get_last_modifier': who_afro_helpers.get_last_modifier,
            'format_locale': who_afro_helpers.format_locale,
            'get_datahub_stats': who_afro_helpers.get_datahub_stats,
            'get_activity_stream_limit': who_afro_helpers.get_activity_stream_limit,
            'get_license': who_afro_helpers.get_license,
            'dataset_has_overview': who_afro_helpers.dataset_has_overview
        }

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "who-afro")

    # IFacets
    def dataset_facets(self, facet_dict, package_type):
        new_facet_dict = OrderedDict()
        new_facet_dict['groups'] = facet_dict['groups']
        new_facet_dict['programme'] = plugins.toolkit._('Programmes')
        new_facet_dict['country'] = plugins.toolkit._('Countries')
        new_facet_dict['tags'] = plugins.toolkit._('Keywords')
        new_facet_dict['res_format'] = plugins.toolkit._('Formats')
        new_facet_dict['organization'] = facet_dict['organization']
        return new_facet_dict

    def group_facets(self, facet_dict, group_type, package_type):
        new_facet_dict = OrderedDict()
        new_facet_dict['programme'] = plugins.toolkit._('Programmes')
        new_facet_dict['country'] = plugins.toolkit._('Countries')
        new_facet_dict['tags'] = plugins.toolkit._('Keywords')
        new_facet_dict['res_format'] = plugins.toolkit._('Formats')
        new_facet_dict['organization'] = facet_dict['organization']
        return new_facet_dict

    def organization_facets(self, facet_dict, organization_type, package_type):
        new_facet_dict = OrderedDict()
        new_facet_dict['groups'] = facet_dict['groups']
        new_facet_dict['programme'] = plugins.toolkit._('Programmes')
        new_facet_dict['country'] = plugins.toolkit._('Countries')
        new_facet_dict['tags'] = plugins.toolkit._('Keywords')
        new_facet_dict['res_format'] = plugins.toolkit._('Formats')
        return new_facet_dict

    # IResourceController
    def before_resource_create(self, context, resource):
        who_afro_upload.handle_giftless_uploads(context, resource)
        return resource

    def before_resource_update(self, context, current, resource):
        who_afro_upload.handle_giftless_uploads(context, resource, current=current)
        return resource

    # IActions
    def get_actions(self):
        return {
            'user_list': who_afro_actions.user_list,
            'dataset_duplicate': who_afro_actions.dataset_duplicate,
            'package_create': who_afro_actions.package_create,
            'dataset_tag_replace': who_afro_actions.dataset_tag_replace,
            'user_show_me': who_afro_actions.user_show_me,
        }

    # IValidators
    def get_validators(self):
        return {
            'autogenerate_name_from_title': who_afro_validators.autogenerate_name_from_title,
            'autofill': who_afro_validators.autofill,
            'autogenerate': who_afro_validators.autogenerate,
            'isomonth': who_afro_validators.isomonth,
            'language_validator': who_afro_validators.language_validator,
            'who_license_autofill': who_afro_validators.who_license_autofill
        }

    # IPackageContoller
    def after_dataset_delete(self, context, data_dict):
        package_data = toolkit.get_action('package_show')(context, data_dict)
        if package_data.get('private'):
            package_data['state'] = 'deleted'
            context['package'].state = 'deleted'
            who_afro_upload.add_activity(context, package_data, "changed")

    def after_dataset_update(self, context, data_dict):
        if data_dict.get('private'):
            who_afro_upload.add_activity(context, data_dict, "changed")

    def after_dataset_create(self, context, data_dict):
        if data_dict.get('private'):
            who_afro_upload.add_activity(context, data_dict, "new")

    def before_dataset_index(self, data_dict: Dict) -> Dict:
        """Load custom multivalued fields as objects before solr indexing.

        Args:
            data_dict (Dict): input data

        Returns:
            Dict: Normalized input data
        """
        if isinstance(data_dict.get('programme'), str):
            data_dict['programme'] = json.loads(data_dict['programme'])
        if isinstance(data_dict.get('country'), str):
            data_dict['country'] = json.loads(data_dict['country'])
        return data_dict

    def get_blueprint(self):
        log.info(f"Registering the following blueprints: {who_afro_blueprints.get_blueprints()}")
        return who_afro_blueprints.get_blueprints()

    # ITranslation
    def i18n_domain(self):
        return 'ckanext-who-afro'
