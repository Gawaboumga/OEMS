from django.test import TestCase, override_settings
from django.urls import reverse
from oems.settings import TEST_MEDIA_ROOT
from api import models
from front import forms
from front.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class PropositionCreationTests(TestCase):

    def test_view_proposition_as_visitor(self):
        utils.log_as(self, utils.UserType.VISITOR)

        url_asked = reverse('front:proposition_creation')
        response = self.client.get(url_asked)
        self.assertRedirects(response, reverse('login') + '?next={}'.format(url_asked))

    def test_user_can_post_proposition(self):
        utils.log_as(self, utils.UserType.USER)

        content = 'test_user_can_post_proposition'

        proposition_form = forms.PropositionForm(data={
            'content': content
        })

        self.assertTrue(proposition_form.is_valid())
        response = self.client.post(reverse('front:proposition_creation'), data=proposition_form.data, format='json')
        self.assertEqual(models.Proposition.objects.count(), 1)
        proposition = models.Proposition.objects.first()

        self.assertRedirects(response, reverse('front:proposition', kwargs={'pk': proposition.pk}))
        self.assertEqual(proposition.content, content)
