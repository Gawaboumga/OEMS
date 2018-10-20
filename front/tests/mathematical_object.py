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

    def test_insert_malicious_markdow_1(self):
        malicious_markdown = """[some text](javascript: alert('xss'))"""

        utils.log_as(self, utils.UserType.STAFF)
        mathematical_object = utils.create_mathematical_object(self, description=malicious_markdown)

        response = self.client.get(reverse('front:mathematical_object', kwargs={'pk': mathematical_object.pk}))
        self.assertNotContains(response, "javascript: alert('xss')")

    def test_insert_malicious_markdown_2(self):
        malicious_markdown = """
        > hello <a name="n"
        > href="javascript:alert('xss')">*you*</a>
        """

        utils.log_as(self, utils.UserType.STAFF)
        mathematical_object = utils.create_mathematical_object(self, description=malicious_markdown)

        response = self.client.get(reverse('front:mathematical_object', kwargs={'pk': mathematical_object.pk}))
        self.assertNotContains(response, "javascript: alert('xss')")

    def test_insert_malicious_markdown_3(self):
        malicious_markdown = """
            [a](javascript:prompt(document.cookie))
            [a](j    a   v   a   s   c   r   i   p   t:prompt(document.cookie))
            ![a](javascript:prompt(document.cookie))\
            <javascript:prompt(document.cookie)>  
            <&#x6A&#x61&#x76&#x61&#x73&#x63&#x72&#x69&#x70&#x74&#x3A&#x61&#x6C&#x65&#x72&#x74&#x28&#x27&#x58&#x53&#x53&#x27&#x29>  
            ![a](data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4K)\
            [a](data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4K)
            [a](&#x6A&#x61&#x76&#x61&#x73&#x63&#x72&#x69&#x70&#x74&#x3A&#x61&#x6C&#x65&#x72&#x74&#x28&#x27&#x58&#x53&#x53&#x27&#x29)
            ![a'"`onerror=prompt(document.cookie)](x)\
            [citelol]: (javascript:prompt(document.cookie))
            [notmalicious](javascript:window.onerror=alert;throw%20document.cookie)
            [test](javascript://%0d%0aprompt(1))
            [test](javascript://%0d%0aprompt(1);com)
        """

        utils.log_as(self, utils.UserType.STAFF)
        #mathematical_object = utils.create_mathematical_object(self, description=malicious_markdown)

        #response = self.client.get(reverse('front:mathematical_object', kwargs={'pk': mathematical_object.pk}))

