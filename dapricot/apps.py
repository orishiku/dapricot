from django.apps import AppConfig

class SimpleDapricotConfig(AppConfig):
    """Simple AppConfig which does not do automatic discovery."""

    name = 'dapricot'
    verbose_name = "Django Apricot"

class DapricotConfig(SimpleDapricotConfig):
    """The default AppConfig for admin which does autodiscovery."""

    def ready(self):
        super().ready()
        self.module.autodiscover()
