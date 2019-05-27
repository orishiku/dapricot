from django.utils.module_loading import autodiscover_modules

def autodiscover():
    autodiscover_modules('dapricot')

default_app_config = 'dapricot.apps.DapricotConfig'