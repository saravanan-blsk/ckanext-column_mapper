"""Controller for the Column name mapping."""
import ckan.lib.base as base
import ckan.lib.helpers as h
import ckan.lib.render
import ckan.logic as logic
import ckan.model as model
import ckan.plugins as p
from ckan.common import request, c
from ckan.lib.base import BaseController

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

        # Create context
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj, 'use_cache': False}

        # Retrieve resource data
        resource_id_dict = {'resource_id': id+'_mapping'}
        try:
            pkg_data = get_action('datastore_search')(context, resource_id_dict)
            c.pkg_data = pkg_data['records']
        except Exception:
            pass

        # Set Form action URL
        c.link = str("/dataset/column-mapper/update/" + id)

        return p.toolkit.render("form/edit_mapping.html")

    def update_mapping(self, id, data=None, errors=None):
        """Update mapping table."""

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'auth_user_obj': c.userobj}

        self.upsert_mapping_data(id, request, context)

        redirect(h.url_for(controller='ckanext.column_mapper.controller:CMController',
                           action='home', id=id))

    def upsert_mapping_data(self, id, request, context):
        """
        Upsert mapping data into the table.
        :param id: str , Id of the resource
        :param request: request Object
        :param context: dict, Context
        """

        resource_id = id + "_mapping"
        counter = 0
        loop_controller = True

        while loop_controller:
            var_names = ['original_name_' + str(counter), 'mapped_name_' + str(counter), 'column_type_' + str(counter)]
            original_name = request.params.get(var_names[0])
            mapped_name = request.params.get(var_names[1])
            column_type = request.params.get(var_names[2])

            table_data = {'resource_id': resource_id, 'records': [{'original_name': original_name,
                                                                   'mapped_name': mapped_name,
                                                                   'column_type': column_type,
                                                                   'resource_id': id}],
                          'method': 'upsert', 'force': True}
            print table_data
            print
            if original_name or mapped_name or column_type:
                get_action('datastore_upsert')(context, table_data)
            else:
                loop_controller = False

            counter += 1
