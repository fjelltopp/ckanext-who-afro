import pytest

from ckan.tests import factories
import ckan.tests.helpers as helpers
from ckan.tests.helpers import call_action
from ckanext.who_afro.plugin import WHOAFROPlugin
from ckanext.who_afro.tests import get_context


@pytest.mark.usefixtures('clean_db', 'with_plugins')
class TestPrivateDatasetActivities():

    def test_activity_is_created_when_creating_private_dataset(self):
        user = factories.User()
        result = call_action(
            'package_create',
            get_context(user['name']),
            name="updated-name",
            private=True,
            owner_org=factories.Organization()['id']
        )
        activity_stream = call_action(
            'package_activity_list',
            get_context(user['name']),
            id=result['id']
        )
        assert len(activity_stream) == 1

    def test_activity_is_created_when_updating_private_dataset(self):
        user = factories.User()
        private_dataset = factories.Dataset(
            private=True,
            owner_org=factories.Organization()['id'],
            creator_user_id=user['id']
        )
        call_action(
            'package_patch',
            get_context(user['name']),
            id=private_dataset['id'],
            name="updated-name"
        )
        activity_stream = call_action(
            'package_activity_list',
            get_context(user['name']),
            id=private_dataset['id']
        )
        assert len(activity_stream) == 1

    def test_activity_is_created_when_deleting_private_dataset(self):
        user = factories.User()
        private_dataset = factories.Dataset(
            private=True,
            owner_org=factories.Organization()['id'],
            creator_user_id=user['id']
        )
        call_action(
            'package_delete',
            get_context(user['name']),
            id=private_dataset['id']
        )
        activity_stream = call_action(
            'package_activity_list',
            get_context(user['name']),
            id=private_dataset['id']
        )
        assert len(activity_stream) == 1


class TestWHOAFROPlugin:
    @pytest.mark.parametrize('input_data, expected_data', [
        (
            {'programme': ['foo', 'bar'], 'country': ['Egypt']},
            {'programme': ['foo', 'bar'], 'country': ['Egypt']}
        ),
        (
            {'programme': '["foo", "bar"]', 'country': '["Egypt"]'},
            {'programme': ['foo', 'bar'], 'country': ['Egypt']}
        )
    ])
    def test_before_dataset_index(self, input_data, expected_data):
        result = WHOAFROPlugin().before_dataset_index(
            input_data
        )
        assert result == expected_data


@pytest.mark.ckan_config("ckan.plugins", "who_afro")
@pytest.mark.usefixtures("with_plugins")
class TestWHOAFROPluginBlueprints:
    def test_terms_blueprint(self, app):
        res = app.get('/terms/')
        assert helpers.body_contains(
            res,
            "The designations and the presentation of the materials used across the data hub websites"
        )
    
    def test_sources_blueprint(self, app):
        res = app.get('/sources/')
        assert helpers.body_contains(
            res,
            "WHO Global Health Data Hub"
        )
        assert helpers.body_contains(
            res,
            "WHO global data health repository with health-related statistics from all member states"
        )
    
    @pytest.mark.parametrize('country', [
        "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cabo Verde",
        "Central African Republic", "Cameroon", "Congo", "Cote d'Ivoire", "Democratic Republic of Congo",
        "Eritrea", "Ethiopia", "Gabon", "Ghana", "Guinea", "Gambia", "Equatorial Guinea", "Guinea-Bissau",
        "Kenya", "Comoros", "Liberia", "Lesotho", "Madagascar", "Mali", "Mauritania", "Mauritius", "Malawi",
        "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Seychelles", "Sierra Leone", "Senegal",
        "South Sudan", "Sao Tome and Principe", "Eswatini", "Chad", "Togo", "United Republic of Tanzania",
        "Uganda", "South Africa", "Zambia", "Zimbabwe"
    ])
    def test_countries_blueprint(self, app, country):
        res = app.get('/countries/')
        assert helpers.body_contains(
            res,
            country
        )
