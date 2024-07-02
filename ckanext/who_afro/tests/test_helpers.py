import pytest
from ckanext.who_afro import helpers as who_afro_helpers


class TestGetLicense():

    @pytest.mark.parametrize("license, expected_title", [
        ('cc-by', 'Creative Commons Attribution'),
        ('other-closed', "Other (Not Open)"),
        ('non-existant-id', None)
    ])
    def test_get_license(self, license, expected_title):
        license_dict = who_afro_helpers.get_license(license)
        assert license_dict.get('title') == expected_title
