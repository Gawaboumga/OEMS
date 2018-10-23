from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from oems.settings import TEST_MEDIA_ROOT
from api import models
from front import forms
from front.views import NUMBER_OF_SIMULTANEOUS_MODIFICATIONS_PER_USER
from front.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class MathematicalObjectDescriptionEditionTests(TestCase):

    def test_edit_description_mathematical_object_as_visitor(self):
        utils.log_as(self, utils.UserType.STAFF)
        mathematical_object = utils.create_mathematical_object(self)

        utils.log_as(self, utils.UserType.VISITOR)
        self.assertFalse(bool(mathematical_object.description))

        new_description = 'edit_no_description_mathematical_object'
        modification_form = forms.ModificationForm(data={
            'new_description': new_description,
        })
        self.assertTrue(modification_form.is_valid())
        url = reverse('front:mathematical_object_description_edition', kwargs={'pk': mathematical_object.pk})
        response = self.client.post(url, modification_form.data, format='json')
        self.assertRedirects(response, reverse('login') + '?next={}'.format(url))

    def test_edit_description_mathematical_object_as_user(self):
        utils.log_as(self, utils.UserType.STAFF)
        mathematical_object = utils.create_mathematical_object(self)

        user = utils.log_as(self, utils.UserType.USER)
        new_description = 'edit_no_description_mathematical_object'
        modification_form = forms.ModificationForm(data={
            'new_description': new_description,
        })
        self.assertTrue(modification_form.is_valid())
        url = reverse('front:mathematical_object_description_edition', kwargs={'pk': mathematical_object.pk})
        response = self.client.post(url, modification_form.data, format='json')

        self.assertEqual(models.Modification.objects.count(), 1)
        created_modification = models.Modification.objects.all()[:1].get()
        self.assertRedirects(response, reverse('front:modification', kwargs={'pk': created_modification.pk}))
        self.assertEqual(created_modification.user, user)

    def test_edit_no_description_mathematical_object(self):
        utils.log_as(self, utils.UserType.STAFF)

        mathematical_object = utils.create_mathematical_object(self)

        self.assertFalse(bool(mathematical_object.description))

        new_description = 'edit_no_description_mathematical_object'
        modification_form = forms.ModificationForm(data={
            'new_description': new_description,
        })
        self.assertTrue(modification_form.is_valid())
        response = self.client.post(reverse('front:mathematical_object_description_edition', kwargs={'pk': mathematical_object.pk}), modification_form.data, format='json')

        self.assertEqual(models.Modification.objects.count(), 1)
        created_modification = models.Modification.objects.all()[:1].get()
        self.assertRedirects(response, reverse('front:modification', kwargs={'pk': created_modification.pk}))
        self.assertEqual(created_modification.get_content(), new_description)
        mathematical_object.refresh_from_db()
        self.assertFalse(bool(mathematical_object.description))

    def test_edit_with_description_mathematical_object(self):
        utils.log_as(self, utils.UserType.STAFF)

        old_description = 'old_test_edit_with_description_mathematical_object'
        mathematical_object = utils.create_mathematical_object(self, description=old_description)

        self.assertEqual(mathematical_object.get_content(), old_description)

        new_description = 'new_test_edit_with_description_mathematical_object'
        modification_form = forms.ModificationForm(data={
            'new_description': new_description,
        })
        self.assertTrue(modification_form.is_valid())
        response = self.client.post(reverse('front:mathematical_object_description_edition', kwargs={'pk': mathematical_object.pk}), modification_form.data, format='json')

        self.assertEqual(models.Modification.objects.count(), 1)
        created_modification = models.Modification.objects.all()[:1].get()
        self.assertRedirects(response, reverse('front:modification', kwargs={'pk': created_modification.pk}))
        self.assertEqual(created_modification.get_content(), new_description)
        mathematical_object.refresh_from_db()
        self.assertEqual(mathematical_object.get_content(), old_description)

    def test_user_can_not_edit_more_than_k_modifications(self):
        utils.log_as(self, utils.UserType.STAFF)
        mathematical_object = utils.create_mathematical_object(self)

        for _ in range(NUMBER_OF_SIMULTANEOUS_MODIFICATIONS_PER_USER):
            response = self.client.post(
                reverse('front:mathematical_object_description_edition', kwargs={'pk': mathematical_object.pk}),
                data={'new_description': 'test_user_can_not_edit_more_than_k_modifications'}, format='json')
            self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        self.assertEqual(models.Modification.objects.count(), NUMBER_OF_SIMULTANEOUS_MODIFICATIONS_PER_USER)

        response = self.client.post(
            reverse('front:mathematical_object_description_edition', kwargs={'pk': mathematical_object.pk}),
            data={'new_description': 'test_user_can_not_edit_more_than_k_modifications'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "error")
        self.assertEqual(models.Modification.objects.count(), NUMBER_OF_SIMULTANEOUS_MODIFICATIONS_PER_USER)
