from django.apps import AppConfig

class SimpleDapricotConfig(AppConfig):
    """Simple AppConfig which does not do automatic discovery."""

    name = 'dapricot.core'
    label = 'dacore'
    verbose_name = "Django Apricot Core Module"

class DapricotCoreConfig(SimpleDapricotConfig):
    """The default AppConfig for admin which does autodiscovery."""

    def ready(self):
        super().ready()
        self.module.autodiscover()
