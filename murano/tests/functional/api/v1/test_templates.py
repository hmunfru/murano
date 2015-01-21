#    Copyright (c) 2014 Mirantis, Inc.
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

from tempest.test import attr
from tempest_lib import exceptions

from murano.tests.functional.api import base


class TestTemplates(base.TestCase):

    @attr(type='smoke')
    def test_list_templates(self):
        resp, body = self.client.get_templates_list()

        self.assertIn('templates', body)
        self.assertEqual(resp.status, 200)

    @attr(type='smoke')
    def test_create_and_delete_templates(self):
        templates_list_start = self.client.get_templates_list()[1]

        resp, temp = self.client.create_templates('test')
        self.templates.append(temp)

        self.assertEqual(resp.status, 200)
        self.assertEqual('test', temp['name'])

        templates_list = self.client.get_templates_list()[1]

        self.assertEqual(len(templates_list_start['templates']) + 1,
                         len(templates_list['templates']))

        self.client.delete_templates(temp['id'])

        templates_list = self.client.get_templates_list()[1]

        self.assertEqual(len(templates_list_start['templates']),
                         len(templates_list['templates']))

        self.templates.pop(self.templates.index(temp))

    @attr(type='smoke')
    def test_get_template(self):
        temp = self.create_template('test')

        resp, template = self.client.get_template(temp['id'])

        self.assertEqual(resp.status, 200)
        self.assertEqual(template['name'], 'test')

    @attr(type='smoke')
    def test_update_template(self):
        temp = self.create_template('test')

        resp, template = self.client.update_template(temp['id'])

        self.assertEqual(resp.status, 200)
        self.assertEqual(template['name'], 'changed-template-name')

    @attr(type='negative')
    def test_update_template_with_wrong_temp_id(self):
        self.assertRaises(exceptions.NotFound,
                          self.client.update_template,
                          None)

    @attr(type='negative')
    def test_delete_template_with_wrong_temp_id(self):
        self.assertRaises(exceptions.NotFound,
                          self.client.delete_template,
                          None)

    @attr(type='negative')
    def test_double_delete_template(self):
        temp = self.create_template('test')

        self.client.delete_templatetemplate(temp['id'])

        self.assertRaises(exceptions.NotFound,
                          self.client.delete_template,
                          temp['id'])

    @attr(type='negative')
    def test_get_deleted_template(self):
        temp = self.create_template('test')

        self.client.delete_template(temp['id'])

        self.assertRaises(exceptions.NotFound,
                          self.client.get_template,
                          temp['id'])


class TestTemplateTenantIsolation(base.NegativeTestCase):

    @attr(type='negative')
    def test_get_template_from_another_tenant(self):
        temp = self.create_template('test')

        self.assertRaises(exceptions.Unauthorized,
                          self.alt_client.get_template, temp['id'])

    @attr(type='negative')
    def test_update_template_from_another_tenant(self):
        temp = self.create_template('test')

        self.assertRaises(exceptions.Unauthorized,
                          self.alt_client.update_template, temp['id'])

    @attr(type='negative')
    def test_delete_template_from_another_tenant(self):
        temp = self.create_template('test')

        self.assertRaises(exceptions.Unauthorized,
                          self.alt_client.delete_template, temp['id'])
