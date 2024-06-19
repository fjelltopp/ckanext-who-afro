import ckanext.who_afro.blueprints.insights as insights
import ckanext.who_afro.blueprints.account as user_account


def get_blueprints():
    return [insights.blueprint, user_account.blueprint]
