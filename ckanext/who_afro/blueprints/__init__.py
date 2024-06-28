import ckanext.who_afro.blueprints.insights as insights
import ckanext.who_afro.blueprints.terms as terms
import ckanext.who_afro.blueprints.dashboard_extension as dashboard_extension


def get_blueprints():
    return [insights.blueprint, terms.blueprint, dashboard_extension.blueprint]
