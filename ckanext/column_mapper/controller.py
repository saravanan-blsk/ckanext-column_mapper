"""Controller for the Column name mapping."""
import ckan.lib.base as base
import ckan.lib.helpers as h
import ckan.lib.render
import ckan.logic as logic
import ckan.model as model
import ckan.plugins as p
from ckan.common import request, c, _
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

    def resource_mapping(self, id, resource_id, data=None, errors=None):
        """Home page for column name mapper."""

        # Create context
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj, 'use_cache': False}

        # Retrieve resource data
        resource_id_dict = {'resource_id': resource_id+'_mapping'}
        try:
            pkg_data = get_action('datastore_search')(context, resource_id_dict)
            pkg_data = pkg_data['records']
            c.pkg_data = sorted(pkg_data, key=lambda k: k.get('_id'))
        except Exception:
            pass

        pkg_dict = get_action('package_show')(context, {'id': id})
        try:
            resource_dict = get_action('resource_show')(context,
                                                        {'id': resource_id})
        except NotFound:
            abort(404, _('Resource not found'))

        c.pkg_dict = pkg_dict
        c.resource = resource_dict

        # Set Form action URL
        c.link = h.url_for(controller='ckanext.column_mapper.controller:CMController',
                           action='resource_mapping_update', id=id, resource_id=resource_id)

        # return p.toolkit.render("form/edit_mapping.html")
        return p.toolkit.render("package/resource_mapping.html")

    def resource_mapping_update(self, id, resource_id, data=None, errors=None):
        """Update mapping table."""

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'auth_user_obj': c.userobj}

        try:
            self.upsert_mapping_data(resource_id, request, context)
        except Exception, e:
            abort(500, _('Failed to update Column mapping - %s') % str(e))

        h.flash_notice(_('Mapping has been updated.'))

        redirect(h.url_for(controller='ckanext.datapusher.plugin:ResourceDataController',
                           action='resource_data', id=id, resource_id=resource_id))

    def resource_mapping_delete(self, id, resource_id):
        """Delete mapping table."""

        if 'cancel' in request.params:
            h.redirect_to(controller='ckanext.column_mapper.controller:CMController',
                          action='resource_mapping',
                          resource_id=resource_id, id=id)

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'auth_user_obj': c.userobj}

        try:
            check_access('package_delete', context, {'id': id})
        except NotAuthorized:
            abort(403, _('Unauthorized to delete package %s') % '')

        try:
            if request.method == 'POST':
                mapping_id = resource_id + '_mapping'
                get_action('datastore_delete')(context, {'resource_id': mapping_id, 'force': True})
                h.flash_notice(_('Mapping has been deleted.'))
                h.redirect_to(controller='ckanext.datapusher.plugin:ResourceDataController',
                              action='resource_data', id=id, resource_id=resource_id)
            c.resource_dict = get_action('resource_show')(
                context, {'id': resource_id})
            c.pkg_id = id
        except NotAuthorized:
            abort(403, _('Unauthorized to delete column mapping %s') % '')
        except NotFound:
            abort(404, _('Column Mapping not found for resource'))
        return render('package/confirm_delete_resource_mapping.html',
                      {'dataset_type': self._get_package_type(id)})

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
                          'method': 'update', 'force': True}

            if original_name or mapped_name or column_type:
                get_action('datastore_upsert')(context, table_data)
            else:
                loop_controller = False

            counter += 1

    def _get_package_type(self, id):
        """
        Given the id of a package this method will return the type of the
        package, or 'dataset' if no type is currently set
        """
        pkg = model.Package.get(id)
        if pkg:
            return pkg.type or 'dataset'
        return None