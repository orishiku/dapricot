from django.apps import AppConfig

class SimpleDapricotConfig(AppConfig):
    """Simple AppConfig which does not do automatic discovery."""

    name = 'dapricot.pages'
    label = 'dapages'
    verbose_name = "Django Apricot Pages Module"

class DapricotPagesConfig(SimpleDapricotConfig):
    """The default AppConfig for admin which does autodiscovery."""

    def ready(self):
        super().ready()
        self.module.autodiscover()
