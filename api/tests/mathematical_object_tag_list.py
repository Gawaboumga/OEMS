from rest_framework import status
from rest_framework.test import APITestCase
from django.test import override_settings
from django.urls import reverse
from oems.settings import TEST_MEDIA_ROOT
from api.models import Tag
from api.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class MathematicalObjectTagListTests(APITestCase):

    def test_add_tag(self):
        utils.log_as(self, utils.UserType.STAFF)

        mathematical_object = utils.create_mathematical_object(self)

        tag = 'test_add_tag'
        data = {
            'tag': tag
        }

        response = self.client.post(reverse('api:mathematical_object_tags', kwargs={'object_pk': mathematical_object.id}), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        tag_object = Tag.objects.get(pk=response.data['id'])
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(tag_object.tag, tag)
        self.assertEqual(len(mathematical_object.tags.all()), 1)

        utils.log_as(self, utils.UserType.USER)
        response = self.client.post(
            reverse('api:mathematical_object_tags', kwargs={'object_pk': mathematical_object.id}), data=data,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        utils.log_as(self, utils.UserType.VISITOR)
        response = self.client.post(
            reverse('api:mathematical_object_tags', kwargs={'object_pk': mathematical_object.id}), data=data,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_another_tag(self):
        utils.log_as(self, utils.UserType.STAFF)

        mathematical_object = utils.create_mathematical_object(self, with_tag=True)

        tag = 'test_add_another_tag'
        tag_object = utils.add_tag(self, mathematical_object.id, default_tag=tag)
        self.assertEqual(Tag.objects.count(), 2)
        self.assertEqual(tag_object.tag, tag)
        self.assertEqual(len(mathematical_object.tags.all()), 2)

    def test_get_tags(self):
        utils.log_as(self, utils.UserType.STAFF)

        mathematical_object = utils.create_mathematical_object(self, with_tag=True)
        tag_object_1 = utils.add_tag(self, mathematical_object.id)
        tag_object_2 = utils.add_tag(self, mathematical_object.id)

        response = self.client.get(reverse('api:mathematical_object_tags', kwargs={'object_pk': mathematical_object.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        is_found_1 = False
        is_found_2 = False
        for tag in response.data:
            is_found_1 |= tag['id'] == tag_object_1.id
            is_found_2 |= tag['id'] == tag_object_2.id
        self.assertTrue(is_found_1)
        self.assertTrue(is_found_2)
