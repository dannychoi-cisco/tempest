# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 OpenStack, LLC
# All Rights Reserved.
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


from tempest.api.identity.base import DataGenerator
from tempest import clients
from tempest import exceptions
import tempest.test


class BaseObjectTest(tempest.test.BaseTestCase):

    @classmethod
    def setUpClass(cls):
        if not cls.config.service_available.swift:
            skip_msg = ("%s skipped as swift is not available" % cls.__name__)
            raise cls.skipException(skip_msg)
        cls.os = clients.Manager()
        cls.object_client = cls.os.object_client
        cls.container_client = cls.os.container_client
        cls.account_client = cls.os.account_client
        cls.custom_object_client = cls.os.custom_object_client
        cls.os_admin = clients.AdminManager()
        cls.token_client = cls.os_admin.token_client
        cls.identity_admin_client = cls.os_admin.identity_client
        cls.custom_account_client = cls.os.custom_account_client
        cls.os_alt = clients.AltManager()
        cls.object_client_alt = cls.os_alt.object_client
        cls.container_client_alt = cls.os_alt.container_client
        cls.identity_client_alt = cls.os_alt.identity_client

        cls.data = DataGenerator(cls.identity_admin_client)

    @classmethod
    def delete_containers(cls, containers, container_client=None,
                          object_client=None):
        """Remove given containers and all objects in them.

        The containers should be visible from the container_client given.
        Will not throw any error if the containers don't exist.

        :param containers: list of container names to remove
        :param container_client: if None, use cls.container_client, this means
            that the default testing user will be used (see 'username' in
            'etc/tempest.conf')
        :param object_client: if None, use cls.object_client
        """
        if container_client is None:
            container_client = cls.container_client
        if object_client is None:
            object_client = cls.object_client
        for cont in containers:
            try:
                objlist = container_client.list_all_container_objects(cont)
                # delete every object in the container
                for obj in objlist:
                    object_client.delete_object(cont, obj['name'])
                container_client.delete_container(cont)
            except exceptions.NotFound:
                pass