from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from oems.settings import TEST_MEDIA_ROOT
from api import models
from front.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class PropositionTests(TestCase):

    def test_view_proposition_as_staff(self):
        user = utils.log_as(self, utils.UserType.STAFF)

        proposition_object = utils.create_proposition(self, by_user=user)

        response = self.client.get(reverse('front:proposition', kwargs={'pk': proposition_object.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'delete')

    def test_view_propositions_as_lambda(self):
        user = utils.log_as(self, utils.UserType.STAFF)
        proposition_object = utils.create_proposition(self, by_user=user)

        url_asked = reverse('front:proposition', kwargs={'pk': proposition_object.pk})

        utils.log_as(self, utils.UserType.USER)
        response = self.client.get(url_asked)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        utils.log_as(self, utils.UserType.VISITOR)
        response = self.client.get(url_asked)
        self.assertRedirects(response, reverse('login') + '?next={}'.format(url_asked))

    def test_view_propositions_as_creator(self):
        user = utils.log_as(self, utils.UserType.USER)
        proposition_object = utils.create_proposition(self, by_user=user)

        response = self.client.get(reverse('front:proposition', kwargs={'pk': proposition_object.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'delete')

    def test_staff_can_delete_proposition(self):
        user = utils.log_as(self, utils.UserType.USER)
        proposition_object = utils.create_proposition(self, by_user=user)

        self.assertEqual(models.Proposition.objects.count(), 1)

        utils.log_as(self, utils.UserType.STAFF)
        response = self.client.post(reverse('front:proposition', kwargs={'pk': proposition_object.pk}))
        self.assertRedirects(response, reverse('front:propositions'))
        self.assertEqual(models.Proposition.objects.count(), 0)

    def test_own_creator_can_delete_proposition(self):
        user = utils.log_as(self, utils.UserType.USER)
        proposition_object = utils.create_proposition(self, by_user=user)

        self.assertEqual(models.Proposition.objects.count(), 1)

        response = self.client.post(reverse('front:proposition', kwargs={'pk': proposition_object.pk}))
        self.assertRedirects(response, reverse('front:index'))
        self.assertEqual(models.Proposition.objects.count(), 0)

    def test_other_user_can_not_delete_proposition(self):
        user = utils.log_as(self, utils.UserType.USER)
        proposition_object = utils.create_proposition(self, by_user=user)

        self.assertEqual(models.Proposition.objects.count(), 1)

        other_user = utils.log_as(self, utils.UserType.USER)
        self.assertNotEqual(user, other_user)
        url_asked = reverse('front:proposition', kwargs={'pk': proposition_object.pk})
        response = self.client.post(url_asked)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(models.Proposition.objects.count(), 1)

        utils.log_as(self, utils.UserType.VISITOR)
        response = self.client.post(url_asked)
        self.assertRedirects(response, reverse('login') + '?next={}'.format(url_asked))

        self.assertEqual(models.Proposition.objects.count(), 1)
