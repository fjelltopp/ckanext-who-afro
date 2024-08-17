import re
import logging
import requests
import csv
from flask import Blueprint
from ckan.plugins import toolkit


log = logging.getLogger(__name__)

blueprint = Blueprint(
    "countries", __name__, url_prefix="/countries"
)


@blueprint.get("/", endpoint="index")
def featured_countries():
    return toolkit.render("countries/index.html")


def _load_country_data() -> dict:
    country_data_url = toolkit.config.get('country_data_url')
    if not country_data_url:
        raise toolkit.ObjectNotFound("No country data file url specified")
    try:
        if country_data_url.startswith('file://'):
            with open(country_data_url.replace('file://', ''), 'r') as f:
                reader = csv.DictReader(f)
                country_data = {row['iso2_code']: row for row in reader}
        else:
            msg = f"Country data must be a local file - urls not yet supported {country_data_url}"
            raise Exception(msg)
            # TODO: Below currently times out - because there's only one thread?
            # timeout = toolkit.config.get('ckan.requests.timeout')
            # response = requests.get(country_data_url, timeout=timeout)
            # reader = csv.DictReader(response.raw)
            # country_data = {row['iso2_code']: row for row in reader}
    except (FileNotFoundError, requests.RequestException) as e:
        msg = f"Couldn't get the country data file {country_data_url}: {e}"
        raise toolkit.ObjectNotFound(msg)
    except KeyError as e:
        msg = f"Does the country data file include column {e}?"
        raise KeyError(msg)
    return country_data


def _extract_src(html_string, default_val):
    src_pattern = r'src="([^"]+)"'
    match = re.search(src_pattern, html_string)
    return match.group(1) if match else default_val


def country(country_id=None, dashboard_id='uhc'):
    country_data = _load_country_data()
    try:
        country_data = country_data[country_id]
    except KeyError:
        return toolkit.abort(
            404,
            toolkit._(f'Country data not found for {country_id}')
        )
    try:
        dashboard = country_data[f'{dashboard_id}_dashboard']
    except KeyError:
        return toolkit.abort(
            404,
            toolkit._(f'Dashboard {dashboard_id} not found for {country_id}')
        )
    default_val = "Unfound"
    template_vars = {
        'iso2_code': country_data.get('iso2_code', default_val),
        'name': country_data.get('name', default_val),
        'flag_url': country_data.get('flag_url', default_val),
        'size_km2': country_data.get('size_km2', default_val),
        'demographic_growth_perc': country_data.get('demographic_growth_perc', default_val),
        'population_size': country_data.get('population_size', default_val),
        'dashboard': _extract_src(dashboard, default_val),
        'uhc_dashboard': _extract_src(country_data['uhc_dashboard'], default_val),
        'hse_dashboard': _extract_src(country_data['hse_dashboard'], default_val),
        'hpop_dashboard': _extract_src(country_data['hpop_dashboard'], default_val),
        'ccs': country_data.get('ccs', default_val),
    }
    return toolkit.render(
        "countries/country.html",
        template_vars
    )


@blueprint.get("/<country_id>")
@blueprint.get("/<country_id>/uhc")
def country_uhc(country_id=None):
    return country(country_id, 'uhc')


@blueprint.get("/<country_id>/hse")
def country_hse(country_id=None):
    return country(country_id, 'hse')


@blueprint.get("/<country_id>/hpop")
def country_hpop(country_id=None):
    return country(country_id, 'hpop')

