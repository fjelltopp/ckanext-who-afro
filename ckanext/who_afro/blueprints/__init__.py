import ckanext.who_afro.blueprints.insights as insights
import ckanext.who_afro.blueprints.terms as terms


def get_blueprints():
    return [insights.blueprint, terms.blueprint]
