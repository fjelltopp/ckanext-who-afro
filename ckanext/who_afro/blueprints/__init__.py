import ckanext.who_afro.blueprints.insights as insights
import ckanext.who_afro.blueprints.countries as countries
import ckanext.who_afro.blueprints.terms as terms


def get_blueprints():
    return [insights.blueprint, countries.blueprint, terms.blueprint]
