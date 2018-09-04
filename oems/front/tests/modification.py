from django.test import TestCase, override_settings
from django.urls import reverse
from oems.settings import TEST_MEDIA_ROOT
from api import models
from front.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class ModificationTests(TestCase):

    def test_view_modification(self):
        utils.login(self)
        mathematical_object = utils.create_mathematical_object(self)
        modification_object = utils.create_modification(self, mathematical_object)

        response = self.client.get(reverse('front:modification', kwargs={'pk': modification_object.pk}))

        self.assertContains(response, mathematical_object.get_content())
        self.assertContains(response, modification_object.get_content())

    def test_accept_modification(self):
        utils.login(self)
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
        utils.login(self)
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
