import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class Column_MapperPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)

    # IRoutes

    def before_map(self, map):
        """
        Called before the routes map is generated. ``before_map`` is before any
        other mappings are created so can override all other mappings.

        :param map: Routes map object
        :returns: Modified version of the map object
        """
        map.connect('resource_mapping', '/dataset/{id}/resource/{resource_id}/mapping',
                    controller='ckanext.column_mapper.controller:CMController',
                    action='resource_mapping',
                    ckan_icon='table')

        map.connect('resource_mapping_update', '/dataset/{id}/resource/{resource_id}/mapping/update',
                    controller='ckanext.column_mapper.controller:CMController',
                    action='resource_mapping_update',
                    ckan_icon='table')

        return map

    def after_map(self, map):
        """
        Called after routes map is set up. ``after_map`` can be used to
        add fall-back handlers.

        :param map: Routes map object
        :returns: Modified version of the map object
        """
        map.connect('resource_mapping', '/dataset/{id}/resource/{resource_id}/mapping',
                    controller='ckanext.column_mapper.controller:CMController',
                    action='resource_mapping',
                    ckan_icon='table')

        map.connect('resource_mapping_update', '/dataset/{id}/resource/{resource_id}/mapping/update',
                    controller='ckanext.column_mapper.controller:CMController',
                    action='resource_mapping_update',
                    ckan_icon='table')

        return map

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'column_mapper')
