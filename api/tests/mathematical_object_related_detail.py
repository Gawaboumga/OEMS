from rest_framework import status
from rest_framework.test import APITestCase
from django.test import override_settings
from django.urls import reverse
from oems.settings import TEST_MEDIA_ROOT
from api.models import Name
from api.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class MathematicalObjectRelatedDetailTests(APITestCase):

    def test_retrieve_specific_relation(self):
        mathematical_object_1 = utils.create_mathematical_object(self)
        mathematical_object_2 = utils.create_mathematical_object(self)
        utils.add_relation(self, mathematical_object_1.id, mathematical_object_2.id)

        self.assertEqual(mathematical_object_1.related.count(), 1)
        self.assertEqual(mathematical_object_2.related.count(), 1)

        response = self.client.delete(reverse('api:mathematical_object_relation', kwargs={'object_pk': mathematical_object_1.id,
                                                                        'other_pk': mathematical_object_2.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(mathematical_object_1.related.count(), 0)
        self.assertEqual(mathematical_object_2.related.count(), 0)
        self.assertEqual(Name.objects.count(), 0)
