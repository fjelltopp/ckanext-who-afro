import ckanext.who_afro.blueprints.insights as insights
import ckanext.who_afro.blueprints.terms as terms
import ckanext.who_afro.blueprints.userflow as userflow


def get_blueprints():
    return [insights.blueprint, terms.blueprint, userflow.blueprint]
