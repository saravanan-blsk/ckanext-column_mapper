"""Controller for the Column name mapping."""
from ckan.lib.base import BaseController
import ckan.logic as logic
import ckan.lib.base as base
import ckan.plugins as p
import ckan.lib.render

render = base.render


class CMController(BaseController):

    def home(self):
        """Home page for column name mapper."""
        return p.toolkit.render("home.html")
