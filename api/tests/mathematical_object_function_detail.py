from rest_framework import status
from rest_framework.test import APITestCase
from django.test import override_settings
from django.urls import reverse
from oems.settings import TEST_MEDIA_ROOT
from api.models import Function
from api.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class MathematicalObjectFunctionDetailTests(APITestCase):

    def test_retrieve_specific_function(self):
        utils.log_as(self, utils.UserType.STAFF)

        mathematical_object = utils.create_mathematical_object(self)
        function_object = utils.add_function(self, mathematical_object.id)

        response = self.client.delete(reverse('api:mathematical_object_function', kwargs={'object_pk': mathematical_object.id,
                                                                        'function_pk': function_object.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(mathematical_object.functions.count(), 0)
        self.assertEqual(Function.objects.count(), 0)

    def test_retrieve_specific_function_as_user_or_visitor(self):
        utils.log_as(self, utils.UserType.STAFF)

        mathematical_object = utils.create_mathematical_object(self)
        function_object = utils.add_function(self, mathematical_object.id)

        utils.log_as(self, utils.UserType.USER)
        response = self.client.delete(reverse('api:mathematical_object_function', kwargs={'object_pk': mathematical_object.id,
                                                                        'function_pk': function_object.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        utils.log_as(self, utils.UserType.VISITOR)
        response = self.client.delete(
            reverse('api:mathematical_object_function', kwargs={'object_pk': mathematical_object.id,
                                                                'function_pk': function_object.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
