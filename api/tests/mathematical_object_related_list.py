from rest_framework import status
from rest_framework.test import APITestCase
from django.test import override_settings
from django.urls import reverse
from oems.settings import TEST_MEDIA_ROOT
from api.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class MathematicalObjectRelatedListTests(APITestCase):

    def test_add_relation(self):
        utils.log_as(self, utils.UserType.STAFF)

        mathematical_object_1 = utils.create_mathematical_object(self)
        mathematical_object_2 = utils.create_mathematical_object(self)

        utils.add_relation(self, mathematical_object_1.id, mathematical_object_2.id)
        mathematical_object_2.refresh_from_db()
        self.assertEqual(mathematical_object_1.related.count(), 1)
        self.assertEqual(mathematical_object_2.related.count(), 1)

    def test_add_another_relation(self):
        utils.log_as(self, utils.UserType.STAFF)

        mathematical_object_1 = utils.create_mathematical_object(self)
        mathematical_object_2 = utils.create_mathematical_object(self)
        mathematical_object_3 = utils.create_mathematical_object(self)

        utils.add_relation(self, mathematical_object_1.id, mathematical_object_2.id)
        utils.add_relation(self, mathematical_object_1.id, mathematical_object_3.id)
        self.assertEqual(mathematical_object_1.related.count(), 2)
        self.assertEqual(mathematical_object_2.related.count(), 1)

    def test_get_relations(self):
        utils.log_as(self, utils.UserType.STAFF)

        mathematical_object_1 = utils.create_mathematical_object(self)
        mathematical_object_2 = utils.create_mathematical_object(self)
        mathematical_object_3 = utils.create_mathematical_object(self)

        utils.add_relation(self, mathematical_object_1.id, mathematical_object_2.id)
        utils.add_relation(self, mathematical_object_1.id, mathematical_object_3.id)

        response = self.client.get(reverse('api:mathematical_object_relations', kwargs={'object_pk': mathematical_object_1.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        is_found_1 = False
        is_found_2 = False
        for relation in response.data:
            is_found_1 |= relation['id'] == mathematical_object_2.id
            is_found_2 |= relation['id'] == mathematical_object_3.id
        self.assertTrue(is_found_1)
        self.assertTrue(is_found_2)
