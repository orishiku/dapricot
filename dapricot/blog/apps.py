from django.apps import AppConfig

class SimpleDapricotBlogConfig(AppConfig):
    """Simple AppConfig which does not do automatic discovery."""

    name = 'dapricot.blog'
    label = 'dablog' #TODO:migration
    verbose_name = "Django Apricot Blog Module"

class DapricotBlogConfig(SimpleDapricotBlogConfig):
    """The default AppConfig for admin which does autodiscovery."""

    def ready(self):
        super().ready()
        self.module.autodiscover()
