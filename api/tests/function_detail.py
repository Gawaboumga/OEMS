from rest_framework import status
from rest_framework.test import APITestCase
from django.test import override_settings
from django.urls import reverse
from oems.settings import TEST_MEDIA_ROOT
from api.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class FunctionDetailTests(APITestCase):

    def test_retrieve_function(self):
        utils.log_as(self, utils.UserType.STAFF)

        mathematical_object = utils.create_mathematical_object(self)
        function_object = utils.add_function(self, mathematical_object.id)

        response = self.client.get(reverse('api:function', kwargs={'pk': function_object.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_two_function(self):
        utils.log_as(self, utils.UserType.STAFF)

        mathematical_object_1 = utils.create_mathematical_object(self)
        function_object = utils.add_function(self, mathematical_object_1.id)
        mathematical_object_2 = utils.create_mathematical_object(self)
        mathematical_object_2.functions.add(function_object)

        response = self.client.get(reverse('api:function', kwargs={'pk': function_object.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_function_as_visitor_and_user(self):
        utils.log_as(self, utils.UserType.STAFF)

        mathematical_object = utils.create_mathematical_object(self)
        function_object = utils.add_function(self, mathematical_object.id)

        utils.log_as(self, utils.UserType.VISITOR)
        response = self.client.get(reverse('api:function', kwargs={'pk': function_object.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        utils.log_as(self, utils.UserType.USER)
        response = self.client.get(reverse('api:function', kwargs={'pk': function_object.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_function(self):
        utils.log_as(self, utils.UserType.STAFF)

        mathematical_object = utils.create_mathematical_object(self)
        function_object = utils.add_function(self, mathematical_object.id)

        new_name = 'test_put_function'
        data = {
            'function': new_name
        }

        response = self.client.put(reverse('api:function', kwargs={'pk': function_object.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        function_object.refresh_from_db()
        self.assertEqual(function_object.function, new_name)

    def test_put_function_as_visitor_and_user(self):
        utils.log_as(self, utils.UserType.STAFF)

        mathematical_object = utils.create_mathematical_object(self)
        function_object = utils.add_function(self, mathematical_object.id)

        new_name = 'test_put_function_as_visitor_and_user'
        data = {
            'function': new_name
        }

        utils.log_as(self, utils.UserType.VISITOR)
        response = self.client.put(reverse('api:function', kwargs={'pk': function_object.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        utils.log_as(self, utils.UserType.USER)
        response = self.client.put(reverse('api:function', kwargs={'pk': function_object.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_one_function(self):
        utils.log_as(self, utils.UserType.STAFF)

        mathematical_object = utils.create_mathematical_object(self)
        function_object_1 = utils.add_function(self, mathematical_object.id)
        function_object_2 = utils.add_function(self, mathematical_object.id)
        self.assertEqual(mathematical_object.functions.count(), 2)

        response = self.client.delete(reverse('api:function', kwargs={'pk': function_object_1.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(mathematical_object.functions.count(), 1)
        self.assertEqual(len(mathematical_object.functions.filter(pk=function_object_2.id)), 1)

    def test_delete_function_as_visitor_and_user(self):
        utils.log_as(self, utils.UserType.STAFF)

        mathematical_object = utils.create_mathematical_object(self)
        function_object = utils.add_function(self, mathematical_object.id)

        utils.log_as(self, utils.UserType.VISITOR)
        response = self.client.delete(reverse('api:function', kwargs={'pk': function_object.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        utils.log_as(self, utils.UserType.USER)
        response = self.client.delete(reverse('api:function', kwargs={'pk': function_object.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
