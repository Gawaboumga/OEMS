from rest_framework import status
from rest_framework.test import APITestCase
from django.test import override_settings
from django.urls import reverse
from oems.settings import TEST_MEDIA_ROOT
from api.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class NameDetailTests(APITestCase):

    def test_retrieve_name(self):
        utils.log_as(self, utils.UserType.STAFF)
        
        mathematical_object = utils.create_mathematical_object(self)
        name_object = utils.add_name(self, mathematical_object.id)

        response = self.client.get(reverse('api:name', kwargs={'pk': name_object.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_two_name(self):
        utils.log_as(self, utils.UserType.STAFF)
        
        mathematical_object_1 = utils.create_mathematical_object(self)
        name_object = utils.add_name(self, mathematical_object_1.id)
        mathematical_object_2 = utils.create_mathematical_object(self)
        mathematical_object_2.names.add(name_object)

        response = self.client.get(reverse('api:name', kwargs={'pk': name_object.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
    def test_retrieve_name_as_visitor_and_user(self):
        utils.log_as(self, utils.UserType.STAFF)

        mathematical_object = utils.create_mathematical_object(self)
        name_object = utils.add_name(self, mathematical_object.id)

        utils.log_as(self, utils.UserType.VISITOR)
        response = self.client.get(reverse('api:name', kwargs={'pk': name_object.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        utils.log_as(self, utils.UserType.USER)
        response = self.client.get(reverse('api:name', kwargs={'pk': name_object.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_name(self):
        utils.log_as(self, utils.UserType.STAFF)
        
        mathematical_object = utils.create_mathematical_object(self)
        name_object = utils.add_name(self, mathematical_object.id)

        new_name = 'test_put_name'
        data = {
            'name': new_name
        }

        response = self.client.put(reverse('api:name', kwargs={'pk': name_object.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        name_object.refresh_from_db()
        self.assertEqual(name_object.name, new_name)

    def test_put_name_as_visitor_and_user(self):
        utils.log_as(self, utils.UserType.STAFF)

        mathematical_object = utils.create_mathematical_object(self)
        name_object = utils.add_name(self, mathematical_object.id)

        new_name = 'test_put_name_as_visitor_and_user'
        data = {
            'function': new_name
        }

        utils.log_as(self, utils.UserType.VISITOR)
        response = self.client.put(reverse('api:name', kwargs={'pk': name_object.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        utils.log_as(self, utils.UserType.USER)
        response = self.client.put(reverse('api:name', kwargs={'pk': name_object.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_one_name(self):
        utils.log_as(self, utils.UserType.STAFF)
        
        mathematical_object = utils.create_mathematical_object(self)
        name_object_1 = utils.add_name(self, mathematical_object.id)
        name_object_2 = utils.add_name(self, mathematical_object.id)
        self.assertEqual(mathematical_object.names.count(), 2)

        response = self.client.delete(reverse('api:name', kwargs={'pk': name_object_1.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(mathematical_object.names.count(), 1)
        self.assertEqual(len(mathematical_object.names.filter(pk=name_object_2.id)), 1)

    def test_delete_name_as_visitor_and_user(self):
        utils.log_as(self, utils.UserType.STAFF)

        mathematical_object = utils.create_mathematical_object(self)
        name_object = utils.add_name(self, mathematical_object.id)

        utils.log_as(self, utils.UserType.VISITOR)
        response = self.client.delete(reverse('api:name', kwargs={'pk': name_object.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        utils.log_as(self, utils.UserType.USER)
        response = self.client.delete(reverse('api:name', kwargs={'pk': name_object.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
