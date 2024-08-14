import logging

from flask import Blueprint
from ckan.plugins import toolkit

log = logging.getLogger(__name__)

blueprint = Blueprint(
    "countries", __name__, url_prefix="/countries"
)


@blueprint.get("/", endpoint="index")
def featured_countries():
    return toolkit.render("countries/index.html")


@blueprint.get("/<country_id>")
def country(country_id=None):
    template_vars = {
        'iso2_code': 'DZ',
        'name': 'Algeria',
        'flag_url': '/images/country-flags/algeria.png',
        'size_km2': '2381741 (2021)',
        'demographic_growth_perc': '3.2 (2022)',
        'population_size': '44903225 (2022)',
        'uhc_dashboard': 'https://app.powerbi.com/view?r=eyJrIjoiYTQ5NjE1YmMtZmZiOC00NGYzLTkwYzMtMDczYjUzMGMwNzdmIiwidCI6ImY2MTBjMGI3LWJkMjQtNGIzOS04MTBiLTNkYzI4MGFmYjU5MCIsImMiOjh9',
        'hse_dashboard': 'https://app.powerbi.com/view?r=eyJrIjoiNjNhMmYwYzEtODVmMC00OWQzLTkwZGItZjk2MDkxODAyZTBiIiwidCI6ImY2MTBjMGI3LWJkMjQtNGIzOS04MTBiLTNkYzI4MGFmYjU5MCIsImMiOjh9',
        'hpop_dashboard': 'https://app.powerbi.com/view?r=eyJrIjoiYmUyMmE3ZTgtOWE5YS00M2U2LThkYTMtNzMzNjI3ZTEyNmUxIiwidCI6ImY2MTBjMGI3LWJkMjQtNGIzOS04MTBiLTNkYzI4MGFmYjU5MCIsImMiOjh9'
    }
    return toolkit.render(
        "countries/country.html",
        template_vars
    )
