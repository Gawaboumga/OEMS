from rest_framework import status
from rest_framework.test import APITestCase
from django.test import override_settings
from django.urls import reverse
from oems.settings import TEST_MEDIA_ROOT
from api.models import Name
from api.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class MathematicalObjectNameDetailTests(APITestCase):

    def test_retrieve_specific_name(self):
        utils.log_as(self, utils.UserType.STAFF)

        mathematical_object = utils.create_mathematical_object(self)
        name_object = utils.add_name(self, mathematical_object.id)

        response = self.client.delete(reverse('api:mathematical_object_name', kwargs={'object_pk': mathematical_object.id,
                                                                        'name_pk': name_object.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(mathematical_object.names.count(), 0)
        self.assertEqual(Name.objects.count(), 0)

    def test_retrieve_specific_name_as_user_or_visitor(self):
        utils.log_as(self, utils.UserType.STAFF)

        mathematical_object = utils.create_mathematical_object(self)
        name_object = utils.add_name(self, mathematical_object.id)

        utils.log_as(self, utils.UserType.USER)
        response = self.client.delete(reverse('api:mathematical_object_name', kwargs={'object_pk': mathematical_object.id,
                                                                        'name_pk': name_object.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        utils.log_as(self, utils.UserType.VISITOR)
        response = self.client.delete(
            reverse('api:mathematical_object_name', kwargs={'object_pk': mathematical_object.id,
                                                                'name_pk': name_object.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
