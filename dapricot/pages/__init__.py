from django.utils.module_loading import autodiscover_modules

def autodiscover():
    autodiscover_modules('dapricot.pages')

default_app_config = 'dapricot.pages.apps.DapricotPagesConfig'