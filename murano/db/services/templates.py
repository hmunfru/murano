# Copyright (c) 2013 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from murano.common import uuidutils
from murano.db import models

from murano.db import session as db_session


DEFAULT_NETWORKS = {
    'template': 'io.murano.resources.NeutronNetwork',
}


class TemplateServices(object):
    @staticmethod
    def get_templates_by(filters):
        """Returns list of environments
           :param filters: property filters
           :return: Returns list of environments
        """
        unit = db_session.get_session()
        templates = unit.query(models.Template). \
            filter_by(**filters).all()

        return templates

    @staticmethod
    def create(template_params, tenant_id):
        #tagging environment by tenant_id for later checks
        """Creates template with specified params, in particular - name

           :param template_params: Dict, e.g. {'name': 'temp-name'}
           :param tenant_id: Tenant Id
           :return: Created Template
        """

        objects = {'?': {
            'id': uuidutils.generate_uuid(),
        }}
        objects.update(template_params)
        objects.update(
            TemplateServices.generate_default_networks(objects['name']))
        objects['?']['type'] = 'io.murano.Template'
        template_params['tenant_id'] = tenant_id

        data = {
            'Objects': objects,
            'Attributes': []
        }

        template = models.Template()
        template.update(template_params)

        unit = db_session.get_session()
        with unit.begin():
            unit.add(template)

        #saving environment as Json to itself
        template.update({'description': data})
        template.save(unit)

        return template

    @staticmethod
    def delete(template_id):
        """Deletes template

           :param template_id: Template that is going to be deleted
           :param token: OpenStack auth token
        """

        temp_description = TemplateServices.get_template_description(
            template_id, False)
        temp_description['Objects'] = None
        TemplateServices.save_template_description(
            temp_description, False)

    @staticmethod
    def remove(template_id):
        unit = db_session.get_session()
        template = unit.query(models.Template).get(template_id)
        if template:
            with unit.begin():
                unit.delete(template)

    @staticmethod
    def get_template_description(template_id, inner=True):
        """Returns template description for specified template.

           :param template_id: Template Id
           :param inner: return contents of template rather than whole
            Object Model structure
           :return: Template Description Object
        """
        unit = db_session.get_session()

        temp = (unit.query(models.Template).get(template_id))
        temp_description = temp.description

        if not inner:
            return temp_description
        else:
            return temp_description['Objects']

    @staticmethod
    def save_template_description(template, inner=True):
        """Saves template description to specified session.

           :param environment: Environment Description
           :param inner: save modifications to only content of environment
            rather than whole Object Model structure
        """
        #unit = db_session.get_session()
#        if inner:
#            data = session.description.copy()
#            data['Objects'] = environment
#            session.description = data
#        else:
#            session.description = environment
#        session.save(unit)

    @staticmethod
    def generate_default_networks(temp_name):
        # This is a temporary workaround. Need to find a better way:
        # These objects have to be created in runtime when the environment is
        # deployed for the first time. Currently there is no way to persist
        # such changes, so we have to create the objects on the API side
        return {
            'defaultNetworks': {
                'environment': {
                    '?': {
                        'id': uuidutils.generate_uuid(),
                        'type': DEFAULT_NETWORKS['template']
                    },
                    'name': temp_name + '-network'
                },
                'flat': None
            }
        }

    @staticmethod
    def create_environment(environment_id, token):
        pass
