from django.utils.module_loading import autodiscover_modules

def autodiscover():
    autodiscover_modules('dapricot.media')

default_app_config = 'dapricot.media.apps.DapricotMediaConfig'