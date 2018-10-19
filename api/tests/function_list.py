from rest_framework import status
from rest_framework.test import APITestCase
from django.test import override_settings
from django.urls import reverse
from oems.settings import PAGINATION_SIZE, TEST_MEDIA_ROOT
from api import models
from api.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class FunctionListTests(APITestCase):

    def test_get_paginated_functions(self):
        utils.log_as(self, utils.UserType.STAFF)

        number_of_functions_to_create = PAGINATION_SIZE + 5
        self.__create_multiple_objects_and_functions(number_of_functions_to_create)

        utils.log_as(self, utils.UserType.USER)
        response = self.client.get(reverse('api:functions'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Function.objects.count(), number_of_functions_to_create)
        self.assertEqual(len(response.data['results']), PAGINATION_SIZE)

    def test_get_functions_as_visitor(self):
        utils.log_as(self, utils.UserType.STAFF)

        number_of_functions_to_create = 5
        self.__create_multiple_objects_and_functions(number_of_functions_to_create)

        utils.log_as(self, utils.UserType.VISITOR)
        response = self.client.get(reverse('api:functions'), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_function_as_staff(self):
        utils.log_as(self, utils.UserType.STAFF)

        function_content = 'test_post_function_as_staff'
        data = {
            'function': function_content
        }
        response = self.client.post(reverse('api:functions'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(len(models.Function.objects.all()), 1)
        function = models.Function.objects.all().first()
        self.assertEqual(function.function, function_content)

    def test_post_function_as_user_or_visitor(self):
        utils.log_as(self, utils.UserType.USER)

        function_content = 'test_post_function_as_user_or_visitor'
        data = {
            'function': function_content
        }
        response = self.client.post(reverse('api:functions'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        utils.log_as(self, utils.UserType.VISITOR)
        response = self.client.post(reverse('api:functions'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def __create_multiple_objects_and_functions(self, number_of_functions):
        for i in range(number_of_functions):
            utils.add_function(self)
