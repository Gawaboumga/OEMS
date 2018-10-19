from rest_framework import status
from rest_framework.test import APITestCase
from django.test import override_settings
from django.urls import reverse
from oems.settings import TEST_MEDIA_ROOT
from api.models import Function
from api.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class MathematicalObjectFunctionListTests(APITestCase):

    def test_add_function(self):
        utils.log_as(self, utils.UserType.STAFF)

        mathematical_object = utils.create_mathematical_object(self)

        function = 'test_add_function'
        data = {
            'function': function
        }

        response = self.client.post(reverse('api:mathematical_object_functions', kwargs={'object_pk': mathematical_object.id}), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        function_object = Function.objects.get(pk=response.data['id'])
        self.assertEqual(Function.objects.count(), 1)
        self.assertEqual(function_object.function, function)
        self.assertEqual(len(mathematical_object.functions.all()), 1)

        utils.log_as(self, utils.UserType.USER)
        response = self.client.post(
            reverse('api:mathematical_object_functions', kwargs={'object_pk': mathematical_object.id}), data=data,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        utils.log_as(self, utils.UserType.VISITOR)
        response = self.client.post(
            reverse('api:mathematical_object_functions', kwargs={'object_pk': mathematical_object.id}), data=data,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_another_function(self):
        utils.log_as(self, utils.UserType.STAFF)

        mathematical_object = utils.create_mathematical_object(self, with_function=True)

        function = 'test_add_another_function'
        function_object = utils.add_function(self, mathematical_object.id, function_name=function)
        self.assertEqual(Function.objects.count(), 2)
        self.assertEqual(function_object.function, function)
        self.assertEqual(len(mathematical_object.functions.all()), 2)

    def test_get_functions(self):
        utils.log_as(self, utils.UserType.STAFF)

        mathematical_object = utils.create_mathematical_object(self, with_function=True)
        function_object_1 = utils.add_function(self, mathematical_object.id)
        function_object_2 = utils.add_function(self, mathematical_object.id)

        response = self.client.get(reverse('api:mathematical_object_functions', kwargs={'object_pk': mathematical_object.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        is_found_1 = False
        is_found_2 = False
        for function in response.data:
            is_found_1 |= function['id'] == function_object_1.id
            is_found_2 |= function['id'] == function_object_2.id
        self.assertTrue(is_found_1)
        self.assertTrue(is_found_2)
