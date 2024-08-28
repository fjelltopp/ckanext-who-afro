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
    
    # @pytest.mark.parametrize('country', [
    #     "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cabo Verde",
    #     "Central African Republic", "Cameroon", "Congo", "Cote d'Ivoire", "Democratic Republic of Congo",
    #     "Eritrea", "Ethiopia", "Gabon", "Ghana", "Guinea", "Gambia", "Equatorial Guinea", "Guinea-Bissau",
    #     "Kenya", "Comoros", "Liberia", "Lesotho", "Madagascar", "Mali", "Mauritania", "Mauritius", "Malawi",
    #     "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Seychelles", "Sierra Leone", "Senegal",
    #     "South Sudan", "Sao Tome and Principe", "Eswatini", "Chad", "Togo", "United Republic of Tanzania",
    #     "Uganda", "South Africa", "Zambia", "Zimbabwe"
    # ])
    # def test_featured_countries_blueprint(self, app, country):
    #     res = app.get('/countries/')
    #     assert helpers.body_contains(
    #         res,
    #         country
    #     )
    
    @pytest.mark.parametrize('country_data', [
        ("DZ", "Algeria", {
            "uhc": "https://app.powerbi.com/view?r=eyJrIjoiYTQ5NjE1YmMtZmZiOC00NGYzLTkwYzMtMDczYjUzMGMwNzdmIiwidCI6ImY2MTBjMGI3LWJkMjQtNGIzOS04MTBiLTNkYzI4MGFmYjU5MCIsImMiOjh9",
            "hse": "https://app.powerbi.com/view?r=eyJrIjoiNjNhMmYwYzEtODVmMC00OWQzLTkwZGItZjk2MDkxODAyZTBiIiwidCI6ImY2MTBjMGI3LWJkMjQtNGIzOS04MTBiLTNkYzI4MGFmYjU5MCIsImMiOjh9",
            "hpop": "https://app.powerbi.com/view?r=eyJrIjoiYmUyMmE3ZTgtOWE5YS00M2U2LThkYTMtNzMzNjI3ZTEyNmUxIiwidCI6ImY2MTBjMGI3LWJkMjQtNGIzOS04MTBiLTNkYzI4MGFmYjU5MCIsImMiOjh9"
        }),
        ("AO", "Angola", {
            "uhc": "https://app.powerbi.com/view?r=eyJrIjoiNzBmNWJhMzUtMDBjZC00MzUxLWJjNTMtNzFjZTVhYjJmZTk3IiwidCI6ImY2MTBjMGI3LWJkMjQtNGIzOS04MTBiLTNkYzI4MGFmYjU5MCIsImMiOjh9",
            "hse": "https://app.powerbi.com/view?r=eyJrIjoiOTA1MDNiNzItNmNjMC00MTM2LWI0YTEtNjk1MDZkOTYwNGI3IiwidCI6ImY2MTBjMGI3LWJkMjQtNGIzOS04MTBiLTNkYzI4MGFmYjU5MCIsImMiOjh9",
            "hpop": "https://app.powerbi.com/view?r=eyJrIjoiMzNlZWI1ZGYtOTRkMy00ZWE4LWEwMDgtZTZhMjU4MzA5OTI4IiwidCI6ImY2MTBjMGI3LWJkMjQtNGIzOS04MTBiLTNkYzI4MGFmYjU5MCIsImMiOjh9"
        }),
        # ("BJ", "Benin", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("BW", "Botswana", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("BF", "Burkina Faso", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("BI", "Burundi", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("CV", "Cabo Verde", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("CF", "Central African Republic", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("CM", "Cameroon", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("CG", "Congo", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # # It's a bit complicated to compare countries which names contain accented characters
        # # ("CI", "Côte d'Ivoire", {
        # #     "uhc": "",
        # #     "hse": "",
        # #     "hpop": ""
        # # }),
        # ("CD", "Democratic Republic of the Congo", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("ER", "Eritrea", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("ET", "Ethiopia", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("GA", "Gabon", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("GH", "Ghana", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("GN", "Guinea", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("GM", "Gambia", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("GQ", "Equatorial Guinea", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("GW", "Guinea-Bissau", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("KE", "Kenya", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("KM", "Comoros", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("LR", "Liberia", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("LS", "Lesotho", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("MG", "Madagascar", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("ML", "Mali", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("MR", "Mauritania", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("MU", "Mauritius", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("MW", "Malawi", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("MZ", "Mozambique", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("NA", "Namibia", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("NE", "Niger", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("NG", "Nigeria", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("RW", "Rwanda", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("SC", "Seychelles", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("SL", "Sierra Leone", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("SN", "Senegal", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("SS", "South Sudan", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("ST", "Sao Tome and Principe", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("SZ", "Eswatini", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("TD", "Chad", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("TG", "Togo", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("TZ", "United Republic of Tanzania", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("UG", "Uganda", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("ZA", "South Africa", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("ZM", "Zambia", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # }),
        # ("ZW", "Zimbabwe", {
        #     "uhc": "",
        #     "hse": "",
        #     "hpop": ""
        # })
    ])
    def test_country_blueprint(self, app, country_data):
        res = app.get('/countries/%s' % country_data[0])
        assert helpers.body_contains(
            res,
            country_data[1]
        )
        assert helpers.body_contains(
            res,
            country_data[2]["uhc"]
        )
        assert helpers.body_contains(
            res,
            country_data[2]["hse"]
        )
        assert helpers.body_contains(
            res,
            country_data[2]["hpop"]
        )
