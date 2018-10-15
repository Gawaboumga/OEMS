from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from oems.settings import TEST_MEDIA_ROOT
from api import models
from front.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class ModificationTests(TestCase):

    def test_view_modification_as_staff(self):
        utils.log_as(self, utils.UserType.STAFF)
        mathematical_object = utils.create_mathematical_object(self)
        modification_object = utils.create_modification(self, mathematical_object)

        response = self.client.get(reverse('front:modification', kwargs={'pk': modification_object.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertContains(response, mathematical_object.get_content())
        self.assertContains(response, modification_object.get_content())
        self.assertContains(response, "accept_modification")
        self.assertContains(response, "reject_modification")

    def test_view_modification_as_lambda(self):
        utils.log_as(self, utils.UserType.STAFF)
        mathematical_object = utils.create_mathematical_object(self)
        modification_object = utils.create_modification(self, mathematical_object)

        utils.log_as(self, utils.UserType.USER)

        url_asked = reverse('front:modification', kwargs={'pk': modification_object.pk})
        response = self.client.get(url_asked)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        utils.log_as(self, utils.UserType.VISITOR)

        response = self.client.get(url_asked)
        self.assertRedirects(response, reverse('login') + '?next={}'.format(url_asked))

    def test_view_modification_as_creator(self):
        utils.log_as(self, utils.UserType.STAFF)
        mathematical_object = utils.create_mathematical_object(self)
        modification_object = utils.create_modification(self, mathematical_object)

        user = utils.log_as(self, utils.UserType.USER)
        modification_object.user = user
        modification_object.save()

        url_asked = reverse('front:modification', kwargs={'pk': modification_object.pk})
        response = self.client.get(url_asked)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotContains(response, "accept_modification")
        self.assertContains(response, "reject_modification")

    def test_accept_modification(self):
        utils.log_as(self, utils.UserType.STAFF)
        mathematical_object = utils.create_mathematical_object(self)
        new_description = 'test_accept_modification'
        modification_object = utils.create_modification(self, mathematical_object, new_description=new_description)

        response = self.client.post(reverse('front:modification', kwargs={'pk': modification_object.pk}), data={
            'accept_modification': ['Accept']
        }, format='json')

        self.assertRedirects(response, reverse('front:mathematical_object', kwargs={'pk': mathematical_object.pk}))

        response = self.client.get(reverse('front:mathematical_object', kwargs={'pk': mathematical_object.pk}))
        self.assertContains(response, new_description)

        self.assertEquals(models.Modification.objects.count(), 0)

    def test_reject_modification(self):
        utils.log_as(self, utils.UserType.STAFF)
        old_description = 'old_description'
        mathematical_object = utils.create_mathematical_object(self, description=old_description)
        new_description = 'test_reject_modification'
        modification_object = utils.create_modification(self, mathematical_object, new_description=new_description)
        path = modification_object.new_description.path
        self.assertTrue(utils.is_file(path))

        response = self.client.post(reverse('front:modification', kwargs={'pk': modification_object.pk}), data={
            'reject_modification': ['Reject']
        }, format='json')

        self.assertRedirects(response, reverse('front:modifications'))

        response = self.client.get(reverse('front:mathematical_object', kwargs={'pk': mathematical_object.pk}))
        self.assertContains(response, old_description)

        self.assertEquals(models.Modification.objects.count(), 0)
        self.assertFalse(utils.is_file(path))

    def test_post_as_lambda(self):
        utils.log_as(self, utils.UserType.STAFF)
        mathematical_object = utils.create_mathematical_object(self)
        modification_object = utils.create_modification(self, mathematical_object)

        utils.log_as(self, utils.UserType.USER)

        url_asked = reverse('front:modification', kwargs={'pk': modification_object.pk})
        response = self.client.post(url_asked, data={
            'accept_modification': ['Accept']
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post(url_asked, data={
            'reject_modification': ['Reject']
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        utils.log_as(self, utils.UserType.VISITOR)

        response = self.client.post(url_asked, data={
            'accept_modification': ['Accept']
        }, format='json')
        self.assertRedirects(response, reverse('login') + '?next={}'.format(url_asked))

        response = self.client.post(url_asked, data={
            'reject_modification': ['Reject']
        }, format='json')
        self.assertRedirects(response, reverse('login') + '?next={}'.format(url_asked))

    def test_creator_can_reject_but_not_accept(self):
        utils.log_as(self, utils.UserType.STAFF)
        mathematical_object = utils.create_mathematical_object(self)
        modification_object = utils.create_modification(self, mathematical_object)

        user = utils.log_as(self, utils.UserType.USER)
        modification_object.user = user
        modification_object.save()

        url_asked = reverse('front:modification', kwargs={'pk': modification_object.pk})
        response = self.client.post(url_asked, data={
            'accept_modification': ['Accept']
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post(url_asked, data={
            'reject_modification': ['Reject']
        }, format='json')
        self.assertRedirects(response, reverse('front:mathematical_object', kwargs={'pk': mathematical_object.pk}))

