from django.utils.module_loading import autodiscover_modules

def autodiscover():
    autodiscover_modules('dapricot.core')

default_app_config = 'dapricot.core.apps.DapricotCoreConfig'