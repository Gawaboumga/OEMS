from rest_framework import status
from rest_framework.test import APITestCase
from django.test import override_settings
from django.urls import reverse
from oems.settings import PAGINATION_SIZE, TEST_MEDIA_ROOT
from api import models
from api.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class NameListTests(APITestCase):

    def test_get_paginated_names(self):
        utils.log_as(self, utils.UserType.STAFF)

        number_of_names_to_create = PAGINATION_SIZE + 5
        self.__create_multiple_objects_and_names(number_of_names_to_create)

        utils.log_as(self, utils.UserType.USER)
        response = self.client.get(reverse('api:names'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Name.objects.count(), number_of_names_to_create)
        self.assertEqual(len(response.data['results']), PAGINATION_SIZE)

    def test_get_names_as_visitor(self):
        utils.log_as(self, utils.UserType.STAFF)

        number_of_names_to_create = 5
        self.__create_multiple_objects_and_names(number_of_names_to_create)

        utils.log_as(self, utils.UserType.VISITOR)
        response = self.client.get(reverse('api:names'), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_name_as_staff(self):
        utils.log_as(self, utils.UserType.STAFF)

        name_content = 'test_post_name_as_staff'
        data = {
            'name': name_content
        }
        response = self.client.post(reverse('api:names'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(len(models.Name.objects.all()), 1)
        name = models.Name.objects.all().first()
        self.assertEqual(name.name, name_content)

    def test_post_name_as_user_or_visitor(self):
        utils.log_as(self, utils.UserType.USER)

        name_content = 'test_post_name_as_user_or_visitor'
        data = {
            'name': name_content
        }
        response = self.client.post(reverse('api:names'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        utils.log_as(self, utils.UserType.VISITOR)
        response = self.client.post(reverse('api:names'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def __create_multiple_objects_and_names(self, number_of_names):
        for i in range(number_of_names):
            utils.add_name(self)
