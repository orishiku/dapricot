from django.apps import AppConfig

class SimpleDapricotConfig(AppConfig):
    """Simple AppConfig which does not do automatic discovery."""

    name = 'dapricot.webhooks'
    label = 'dahooks'
    verbose_name = "Django Apricot Webhooks Module"

class DapricotWebhooksConfig(SimpleDapricotConfig):
    """The default AppConfig for admin which does autodiscovery."""

    def ready(self):
        super().ready()
        self.module.autodiscover()
