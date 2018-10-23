from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from oems.settings import TEST_MEDIA_ROOT
from api import models
from front import forms
from front.views import NUMBER_OF_SIMULTANEOUS_PROPOSITIONS_PER_USER
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

        response = self.__post_proposition(content)
        self.assertEqual(models.Proposition.objects.count(), 1)
        proposition = models.Proposition.objects.first()

        self.assertRedirects(response, reverse('front:proposition', kwargs={'pk': proposition.pk}))
        self.assertEqual(proposition.content, content)

    def test_user_can_not_post_more_than_k_propositions(self):
        utils.log_as(self, utils.UserType.USER)

        content = 'test_user_can_not_post_more_than_k_propositions'
        for _ in range(NUMBER_OF_SIMULTANEOUS_PROPOSITIONS_PER_USER):
            response = self.__post_proposition(content)
            self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(models.Proposition.objects.count(), NUMBER_OF_SIMULTANEOUS_PROPOSITIONS_PER_USER)

        response = self.__post_proposition(content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "error")
        self.assertEqual(models.Proposition.objects.count(), NUMBER_OF_SIMULTANEOUS_PROPOSITIONS_PER_USER)

    def __post_proposition(self, content):
        proposition_form = forms.PropositionForm(data={
            'content': content
        })

        self.assertTrue(proposition_form.is_valid())
        return self.client.post(reverse('front:proposition_creation'), data=proposition_form.data, format='json')
