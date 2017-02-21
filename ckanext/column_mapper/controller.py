"""Controller for the Column name mapping."""
from ckan.lib.base import BaseController
import ckan.logic as logic
import ckan.lib.base as base
import ckan.plugins as p
import ckan.lib.render
import ckan.lib.helpers as h
from ckan.common import OrderedDict, _, json, request, c, g, response
import ckan.lib.render

render = base.render
abort = base.abort
redirect = base.redirect


class CMController(BaseController):

    def home(self):
        """Home page for column name mapper."""
        return p.toolkit.render("form/edit_mapping.html")
