from rest_framework import status
from rest_framework.test import APITestCase
from django.test import override_settings
from django.urls import reverse
from oems.settings import PAGINATION_SIZE, TEST_MEDIA_ROOT
from api import models
from api.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class TagListTests(APITestCase):

    def test_get_paginated_tags(self):
        utils.log_as(self, utils.UserType.STAFF)

        number_of_tags_to_create = PAGINATION_SIZE + 5
        self.__create_multiple_objects_and_tags(number_of_tags_to_create)

        utils.log_as(self, utils.UserType.USER)
        response = self.client.get(reverse('api:tags'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Tag.objects.count(), number_of_tags_to_create)
        self.assertEqual(len(response.data['results']), PAGINATION_SIZE)

    def test_get_tags_as_visitor(self):
        utils.log_as(self, utils.UserType.STAFF)

        number_of_tags_to_create = 5
        self.__create_multiple_objects_and_tags(number_of_tags_to_create)

        utils.log_as(self, utils.UserType.VISITOR)
        response = self.client.get(reverse('api:tags'), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_tag_as_staff(self):
        utils.log_as(self, utils.UserType.STAFF)

        tag_content = 'test_post_tag_as_staff'
        data = {
            'tag': tag_content
        }
        response = self.client.post(reverse('api:tags'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(len(models.Tag.objects.all()), 1)
        tag = models.Tag.objects.all().first()
        self.assertEqual(tag.tag, tag_content)

    def test_post_tag_as_user_or_visitor(self):
        utils.log_as(self, utils.UserType.USER)

        tag_content = 'test_post_tag_as_user_or_visitor'
        data = {
            'tag': tag_content
        }
        response = self.client.post(reverse('api:tags'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        utils.log_as(self, utils.UserType.VISITOR)
        response = self.client.post(reverse('api:tags'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def __create_multiple_objects_and_tags(self, number_of_tags):
        for i in range(number_of_tags):
            utils.add_tag(self)
