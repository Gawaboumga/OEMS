from rest_framework import status
from django.test import TestCase, override_settings
from django.urls import reverse
from oems.settings import TEST_MEDIA_ROOT
from api import models
from front import forms
from front.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class MathematicalObjectCreationTests(TestCase):

    def test_view_mathematical_object_creation_as_staff(self):
        utils.log_as(self, utils.UserType.STAFF)

        response = self.client.get(reverse('front:mathematical_object_creation'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_mathematical_object_creation_as_non_staff(self):
        utils.log_as(self, utils.UserType.USER)

        url_asked = reverse('front:mathematical_object_creation')
        response = self.client.get(url_asked)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        utils.log_as(self, utils.UserType.VISITOR)

        response = self.client.get(url_asked)
        self.assertRedirects(response, reverse('login') + '?next={}'.format(url_asked))

    def test_create_small_mathematical_object(self):
        utils.log_as(self, utils.UserType.STAFF)

        representation = 'testcreatesmallmathematicalobject'
        type2 = 'S'

        mathematical_object_form = forms.MathematicalObjectForm(data={
            'latex': representation,
            'type': type2
        })
        self.assertTrue(mathematical_object_form.is_valid())
        response = self.client.post(reverse('front:mathematical_object_creation'), data=mathematical_object_form.data, format='json')
        self.assertTrue(status.HTTP_302_FOUND)
        self.assertEqual(models.MathematicalObject.objects.count(), 1)
        created_object = models.MathematicalObject.objects.all()[:1].get()
        self.assertRedirects(response, reverse('front:mathematical_object', kwargs={'pk': created_object.pk}))
        self.assertEqual(created_object.latex, representation)
        self.assertEqual(created_object.type, type2)

    def test_create_partial_mathematical_object_with_function(self):
        utils.log_as(self, utils.UserType.STAFF)
        func = utils.create_function(self)

        representation = 'testcreatepartialmathematicalobjectwithfunction'
        type2 = 'S'

        mathematical_object_form = forms.MathematicalObjectForm(data={
            'latex': representation,
            'type': type2,
            'functions': [func.id]
        })
        self.assertTrue(mathematical_object_form.is_valid())
        response = self.client.post(reverse('front:mathematical_object_creation'), mathematical_object_form.data, format='json')
        self.assertTrue(status.HTTP_302_FOUND)
        self.assertEqual(models.MathematicalObject.objects.count(), 1)
        created_object = models.MathematicalObject.objects.all()[:1].get()
        self.assertRedirects(response, reverse('front:mathematical_object', kwargs={'pk': created_object.pk}))
        self.assertEqual(created_object.latex, representation)
        self.assertEqual(created_object.type, type2)
        self.assertEqual(created_object.functions.count(), 1)
        retrieved_function = models.Function.objects.get(id__in=created_object.functions.all())
        self.assertEqual(func.function, retrieved_function.function)
        self.assertEqual(created_object.names.count(), 0)

    def test_create_partial_mathematical_object_with_name(self):
        utils.log_as(self, utils.UserType.STAFF)
        name = utils.create_name(self)

        representation = 'testcreatepartialmathematicalobjectwithname'
        type2 = 'S'

        mathematical_object_form = forms.MathematicalObjectForm(data={
            'latex': representation,
            'type': type2,
            'names': [name.id]
        })
        self.assertTrue(mathematical_object_form.is_valid())
        response = self.client.post(reverse('front:mathematical_object_creation'), mathematical_object_form.data, format='json')
        self.assertTrue(status.HTTP_302_FOUND)
        self.assertEqual(models.MathematicalObject.objects.count(), 1)
        created_object = models.MathematicalObject.objects.all()[:1].get()
        self.assertRedirects(response, reverse('front:mathematical_object', kwargs={'pk': created_object.pk}))
        self.assertEqual(created_object.latex, representation)
        self.assertEqual(created_object.type, type2)
        self.assertEqual(created_object.names.count(), 1)
        retrieved_name = models.Name.objects.get(id__in=created_object.names.all())
        self.assertEqual(name.name, retrieved_name.name)
        self.assertEqual(created_object.functions.count(), 0)

    def test_create_partial_mathematical_object_with_related(self):
        utils.log_as(self, utils.UserType.STAFF)
        mathematical_object_1 = utils.create_mathematical_object(self, with_name=True, with_function=True)

        representation = 'testcreatefullmathematicalobject'
        type2 = 'S'

        mathematical_object_form = forms.MathematicalObjectForm(data={
            'latex': representation,
            'type': type2,
            'related': [mathematical_object_1.id]
        })
        self.assertTrue(mathematical_object_form.is_valid())
        response = self.client.post(reverse('front:mathematical_object_creation'), mathematical_object_form.data,
                                    format='json')
        self.assertTrue(status.HTTP_302_FOUND)
        self.assertEqual(models.MathematicalObject.objects.count(), 2)
        mathematical_object_2 = models.MathematicalObject.objects.exclude(pk=mathematical_object_1.id)[:1].get()
        self.assertRedirects(response, reverse('front:mathematical_object', kwargs={'pk': mathematical_object_2.pk}))
        self.assertEqual(mathematical_object_2.latex, representation)
        self.assertEqual(mathematical_object_2.type, type2)
        result = mathematical_object_1.related.get(pk=mathematical_object_2.id)
        self.assertEqual(result.latex, representation)

    def test_create_full_mathematical_object(self):
        utils.log_as(self, utils.UserType.STAFF)
        func = utils.create_function(self)
        name = utils.create_name(self)
        mathematical_object_1 = utils.create_mathematical_object(self)

        representation = 'testcreatefullmathematicalobject'
        object_type = 'S'
        description = 'test_create_full_mathematical_object'

        mathematical_object_form = forms.MathematicalObjectForm(data={
            'latex': representation,
            'type': object_type,
            'functions': [func.id],
            'names': [name.id],
            'related': [mathematical_object_1.id],
            'description': description
        })
        self.assertTrue(mathematical_object_form.is_valid())
        response = self.client.post(reverse('front:mathematical_object_creation'), mathematical_object_form.data,
                                    format='json')
        self.assertTrue(status.HTTP_302_FOUND)
        self.assertEqual(models.MathematicalObject.objects.count(), 2)

        mathematical_object_2 = models.MathematicalObject.objects.exclude(pk=mathematical_object_1.id)[:1].get()
        self.assertEqual(mathematical_object_2.get_content(), description)
