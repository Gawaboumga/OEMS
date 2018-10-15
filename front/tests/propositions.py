from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from oems.settings import TEST_MEDIA_ROOT
from front.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class PropositionsTests(TestCase):

    def test_view_propositions_as_staff(self):
        user = utils.log_as(self, utils.UserType.STAFF)

        proposition_object = utils.create_proposition(self, by_user=user)

        response = self.client.get(reverse('front:propositions'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertContains(response, reverse('front:proposition', kwargs={'pk': proposition_object.pk}))

    def test_view_propositions_as_non_staff(self):
        utils.log_as(self, utils.UserType.STAFF)

        url_asked = reverse('front:propositions')

        utils.log_as(self, utils.UserType.USER)
        response = self.client.get(url_asked)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        utils.log_as(self, utils.UserType.VISITOR)
        response = self.client.get(url_asked)
        self.assertRedirects(response, reverse('login') + '?next={}'.format(url_asked))
