from rest_framework import status
from django.test import TestCase, override_settings
from django.urls import reverse
from oems.settings import TEST_MEDIA_ROOT
from api import models
from front import forms
from front.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class MathematicalObjectTests(TestCase):

    def test_view_mathematical_object_as_staff(self):
        utils.log_as(self, utils.UserType.STAFF)
        mathematical_object = utils.create_mathematical_object(self)

        response = self.client.get(reverse('front:mathematical_object', kwargs={'pk': mathematical_object.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, reverse('front:mathematical_object_edition', kwargs={'pk': mathematical_object.pk}))
        self.assertContains(response, reverse('front:mathematical_object_description_edition', kwargs={'pk': mathematical_object.pk}))

    def test_view_mathematical_object_creation_as_user(self):
        utils.log_as(self, utils.UserType.STAFF)
        mathematical_object = utils.create_mathematical_object(self)

        utils.log_as(self, utils.UserType.USER)
        response = self.client.get(reverse('front:mathematical_object', kwargs={'pk': mathematical_object.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotContains(response, reverse('front:mathematical_object_edition', kwargs={'pk': mathematical_object.pk}))
        self.assertContains(response, reverse('front:mathematical_object_description_edition', kwargs={'pk': mathematical_object.pk}))

    def test_view_mathematical_object_creation_as_visitor(self):
        utils.log_as(self, utils.UserType.STAFF)
        mathematical_object = utils.create_mathematical_object(self)

        utils.log_as(self, utils.UserType.VISITOR)
        response = self.client.get(reverse('front:mathematical_object', kwargs={'pk': mathematical_object.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotContains(response, reverse('front:mathematical_object_edition', kwargs={'pk': mathematical_object.pk}))
        self.assertNotContains(response, reverse('front:mathematical_object_description_edition', kwargs={'pk': mathematical_object.pk}))
