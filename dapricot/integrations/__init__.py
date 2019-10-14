from django.utils.module_loading import autodiscover_modules

def autodiscover():
    autodiscover_modules('dapricot.integrations')

default_app_config = 'dapricot.integrations.apps.DapricotIntegrationsConfig'