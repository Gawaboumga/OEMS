from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from oems.settings import TEST_MEDIA_ROOT
from front.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class ModificationsTests(TestCase):

    def test_view_propositions_as_staff(self):
        utils.log_as(self, utils.UserType.STAFF)
        mathematical_object = utils.create_mathematical_object(self)
        modification_object = utils.create_modification(self, mathematical_object)

        response = self.client.get(reverse('front:modifications'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertContains(response, reverse('front:modification', kwargs={'pk': modification_object.pk}))

    def test_view_propositions_as_non_staff(self):
        utils.log_as(self, utils.UserType.STAFF)
        mathematical_object = utils.create_mathematical_object(self)
        modification_object = utils.create_modification(self, mathematical_object)

        url_asked = reverse('front:modifications')

        utils.log_as(self, utils.UserType.USER)
        response = self.client.get(url_asked)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        utils.log_as(self, utils.UserType.VISITOR)
        response = self.client.get(url_asked)
        self.assertRedirects(response, reverse('login') + '?next={}'.format(url_asked))
