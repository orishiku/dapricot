from django.contrib.flatpages.models import FlatPage
from django.db import models
from django.utils.translation import gettext_lazy as _

class Page(FlatPage):
    in_main_menu = models.BooleanField(
        _('show in main menu'),
        help_text=_("If this is checked, the page will be visible in main menu."),
        default=False,
    )
    
    class Meta:
        db_table = 'dapricot_pages_page'
