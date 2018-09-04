from rest_framework import status
from rest_framework.test import APITestCase
from django.test import override_settings
from django.urls import reverse
from oems.settings import TEST_MEDIA_ROOT
from api.models import Name
from api.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class NameListTests(APITestCase):

    def test_get_paginated_functions(self):
        number_of_objects_to_create = 50
        mathematical_object_ids = []
        for i in range(number_of_objects_to_create):
            mathematical_object_ids.append(utils.create_mathematical_object(self).id)

        for i in range(number_of_objects_to_create):
            utils.add_name(self, mathematical_object_ids[i])

        response = self.client.get(reverse('api:names'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Name.objects.count(), number_of_objects_to_create)
        self.assertEqual(len(response.data), number_of_objects_to_create)
