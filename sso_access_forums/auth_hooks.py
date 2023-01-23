from django.utils.translation import gettext_lazy as _

from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

from . import urls
from .constants import Constants

class SsoPluginItem(MenuItemHook):
    """Displays our plugin in Allance Auth's sidebar menu.
    """

    def __init__(self):
        # setup menu entry for sidebar
        MenuItemHook.__init__(
            self,
            _(Constants.app_name_raw),
            "fas fa-cube fa-fw",
            f"{Constants.app_url}:index",
            navactive=[f"{Constants.app_url}:"],
        )

    def render(self, request):
        """Displays the plugin if the requested user
        has appropriate permissions.
        """
        if request.user.has_perm(f"{Constants.app_url}.basic_access"):
            return MenuItemHook.render(self, request)
        return ""


@hooks.register("menu_item_hook")
def register_menu():
    return SsoPluginItem()


@hooks.register("url_hook")
def register_urls():
    return UrlHook(urls, Constants.app_name_raw, f"^{Constants.app_url}/")
