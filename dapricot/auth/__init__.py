from django.utils.module_loading import autodiscover_modules

def autodiscover():
    autodiscover_modules('dapricot.auth')

default_app_config = 'dapricot.auth.apps.DapricotAuthConfig'