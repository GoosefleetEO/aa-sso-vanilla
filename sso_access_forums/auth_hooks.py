from django.utils.translation import gettext_lazy as _

from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

from . import urls
from .constants import Names

class SsoPluginItem(MenuItemHook):
    """Displays our plugin in Allance Auth's sidebar menu.
    """

    def __init__(self):
        # setup menu entry for sidebar
        MenuItemHook.__init__(
            self,
            _(Names.app_name_raw),
            "fas fa-cube fa-fw",
            f"{Constants.app_url}:index",
            navactive=[f"{Names.app_url}:"],
        )

    def render(self, request):
        """Displays the plugin if the requested user
        has appropriate permissions.
        """
        if request.user.has_perm(f"{Names.app_url}.basic_access"):
            return MenuItemHook.render(self, request)
        return ""


@hooks.register("menu_item_hook")
def register_menu():
    return SsoPluginItem()


@hooks.register("url_hook")
def register_urls():
    return UrlHook(urls, Names.app_name_raw, f"^{Names.app_url}/")
