"""Controller for the Column name mapping."""
from ckan.lib.base import BaseController
import ckan.model as model
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


NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
ValidationError = logic.ValidationError
check_access = logic.check_access
get_action = logic.get_action
tuplize_dict = logic.tuplize_dict
clean_dict = logic.clean_dict
parse_params = logic.parse_params
flatten_to_string_key = logic.flatten_to_string_key

lookup_package_plugin = ckan.lib.plugins.lookup_package_plugin


class CMController(BaseController):

    def home(self, id, data=None, errors=None):
        """Home page for column name mapper."""

        # Creating context
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj, 'use_cache': False}

        # Retrieving resource data
        data_dict_dict = {'resource_id': id+'_mapping'}
        pkg_data_dictionary = get_action('datastore_search')(context, data_dict_dict)
        c.pkg_data_dictionary = pkg_data_dictionary['records']

        return p.toolkit.render("form/edit_mapping.html")
