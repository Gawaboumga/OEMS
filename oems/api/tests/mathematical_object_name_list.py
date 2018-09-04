from rest_framework import status
from rest_framework.test import APITestCase
from django.test import override_settings
from django.urls import reverse
from oems.settings import TEST_MEDIA_ROOT
from api.models import Name
from api.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class MathematicalObjectNameListTests(APITestCase):

    def test_add_name(self):
        mathematical_object = utils.create_mathematical_object(self)

        name = 'test_add_name'
        name_object = utils.add_name(self, mathematical_object.id, default_name=name)
        self.assertEqual(Name.objects.count(), 1)
        self.assertEqual(name_object.name, name)
        self.assertEqual(len(mathematical_object.names.all()), 1)

    def test_add_another_name(self):
        mathematical_object = utils.create_mathematical_object(self, with_name=True)

        name = 'test_add_another_name'
        name_object = utils.add_name(self, mathematical_object.id, default_name=name)
        self.assertEqual(Name.objects.count(), 2)
        self.assertEqual(name_object.name, name)
        self.assertEqual(len(mathematical_object.names.all()), 2)

    def test_get_names(self):
        mathematical_object = utils.create_mathematical_object(self, with_name=True)
        name_object_1 = utils.add_name(self, mathematical_object.id)
        name_object_2 = utils.add_name(self, mathematical_object.id)

        response = self.client.get(reverse('api:mathematical_object_names', kwargs={'object_pk': mathematical_object.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        is_found_1 = False
        is_found_2 = False
        for name in response.data:
            is_found_1 |= name['id'] == name_object_1.id
            is_found_2 |= name['id'] == name_object_2.id
        self.assertTrue(is_found_1)
        self.assertTrue(is_found_2)
