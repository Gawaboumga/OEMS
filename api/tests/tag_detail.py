from rest_framework import status
from rest_framework.test import APITestCase
from django.test import override_settings
from django.urls import reverse
from oems.settings import TEST_MEDIA_ROOT
from api.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class NameDetailTests(APITestCase):

    def test_retrieve_tag(self):
        mathematical_object = utils.create_mathematical_object(self)
        tag_object = utils.add_tag(self, mathematical_object.id)

        response = self.client.get(reverse('api:tag', kwargs={'pk': tag_object.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_two_tag(self):
        mathematical_object_1 = utils.create_mathematical_object(self)
        tag_object = utils.add_tag(self, mathematical_object_1.id)
        mathematical_object_2 = utils.create_mathematical_object(self)
        mathematical_object_2.tags.add(tag_object)

        response = self.client.get(reverse('api:tag', kwargs={'pk': tag_object.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_put_tag(self):
        mathematical_object = utils.create_mathematical_object(self)
        tag_object = utils.add_tag(self, mathematical_object.id)

        new_tag = 'test_put_tag'
        data = {
            'tag': new_tag
        }

        response = self.client.put(reverse('api:tag', kwargs={'pk': tag_object.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tag_object.refresh_from_db()
        self.assertEqual(tag_object.tag, new_tag)

    def test_delete_one_tag(self):
        mathematical_object = utils.create_mathematical_object(self)
        tag_object_1 = utils.add_tag(self, mathematical_object.id)
        tag_object_2 = utils.add_tag(self, mathematical_object.id)
        self.assertEqual(mathematical_object.tags.count(), 2)

        response = self.client.delete(reverse('api:tag', kwargs={'pk': tag_object_1.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(mathematical_object.tags.count(), 1)
        self.assertEqual(len(mathematical_object.tags.filter(pk=tag_object_2.id)), 1)
