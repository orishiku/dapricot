from django.apps import AppConfig

class SimpleDapricotConfig(AppConfig):
    """Simple AppConfig which does not do automatic discovery."""

    name = 'dapricot.auth'
    label = 'daauth'#TODO:migration
    verbose_name = "Django Apricot Auth Module"

class DapricotAuthConfig(SimpleDapricotConfig):
    """The default AppConfig for admin which does autodiscovery."""

    def ready(self):
        super().ready()
        self.module.autodiscover()
