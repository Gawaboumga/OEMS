from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import html
from rest_framework import status
from oems.settings import TEST_MEDIA_ROOT
from api import models
from front import forms
from front.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class MathematicalObjectEditionTests(TestCase):

    def test_view_mathematical_object_edition_as_staff(self):
        utils.log_as(self, utils.UserType.STAFF)

        objects, func, name = self.__create_test_data()
        mathematical_object_2 = objects[1]
        response = self.client.get(reverse('front:mathematical_object_edition', kwargs={'pk': mathematical_object_2.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_mathematical_object_edition_as_non_staff(self):
        self.test_view_mathematical_object_edition_as_staff()

        utils.log_as(self, utils.UserType.USER)

        url_asked = reverse('front:mathematical_object_creation')
        response = self.client.get(url_asked)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        utils.log_as(self, utils.UserType.VISITOR)

        response = self.client.get(url_asked)
        self.assertRedirects(response, reverse('login') + '?next={}'.format(url_asked))

    def test_edition_retrieve_all_the_information(self):
        utils.log_as(self, utils.UserType.STAFF)

        description = 'test_edition_retrieve_all_the_information'
        objects, func, name = self.__create_test_data(with_description=description)
        mathematical_object_2 = objects[1]
        response = self.client.get(reverse('front:mathematical_object_edition', kwargs={'pk': mathematical_object_2.pk}))

        self.assertContains(response, mathematical_object_2.latex)
        self.assertContains(response, '<option value="S" selected>SERIES</option>')

        self.assertContains(response, '<option value="{}" selected>{}</option>'.format(func.pk, func.function))
        self.assertContains(response, '<option value="{}" selected>{}</option>'.format(name.pk, name.name))
        for related in mathematical_object_2.related.all():
            self.assertContains(response, '<option value="{}" selected>{}</option>'.format(related.pk, html.escape(related)))

        self.assertContains(response, description)

    def test_change_latex(self):
        utils.log_as(self, utils.UserType.STAFF)

        objects, func, name = self.__create_test_data()
        mathematical_object_2 = objects[1]

        new_latex = 'testadddescription'

        data = {
            'latex': new_latex,
            'type': mathematical_object_2.type,
            'related': [m.pk for m in mathematical_object_2.related.all()],
            'functions': [f.pk for f in mathematical_object_2.functions.all()],
            'names': [n.pk for n in mathematical_object_2.names.all()]
        }
        mathematical_object_form = forms.MathematicalObjectForm(data)
        self.assertTrue(mathematical_object_form.is_valid())
        self.client.post(reverse('front:mathematical_object_edition', kwargs={'pk': mathematical_object_2.pk}), mathematical_object_form.data, format='json')

        mathematical_object_2.refresh_from_db()
        self.assertEqual(mathematical_object_2.latex, new_latex)
        self.assertFalse(mathematical_object_2.get_content())

    def test_add_description(self):
        utils.log_as(self, utils.UserType.STAFF)

        objects, func, name = self.__create_test_data()
        mathematical_object_2 = objects[1]
        self.assertFalse(mathematical_object_2.get_content())

        new_description = 'test_add_description'

        data = {
            'latex': mathematical_object_2.latex,
            'type': mathematical_object_2.type,
            'related': [m.pk for m in mathematical_object_2.related.all()],
            'functions': [f.pk for f in mathematical_object_2.functions.all()],
            'names': [n.pk for n in mathematical_object_2.names.all()],
            'description': new_description
        }
        mathematical_object_form = forms.MathematicalObjectForm(data)
        self.assertTrue(mathematical_object_form.is_valid())
        self.client.post(reverse('front:mathematical_object_edition', kwargs={'pk': mathematical_object_2.pk}), mathematical_object_form.data, format='json')

        mathematical_object_2.refresh_from_db()
        self.assertEqual(mathematical_object_2.get_content(), new_description)

    def test_change_description(self):
        utils.log_as(self, utils.UserType.STAFF)

        old_description = 'old_description'
        objects, func, name = self.__create_test_data(with_description=old_description)
        mathematical_object_2 = objects[1]
        self.assertEqual(mathematical_object_2.get_content(), old_description)

        new_description = 'test_change_description'

        data = {
            'latex': mathematical_object_2.latex,
            'type': mathematical_object_2.type,
            'related': [m.pk for m in mathematical_object_2.related.all()],
            'functions': [f.pk for f in mathematical_object_2.functions.all()],
            'names': [n.pk for n in mathematical_object_2.names.all()],
            'description': new_description
        }
        mathematical_object_form = forms.MathematicalObjectForm(data)
        self.assertTrue(mathematical_object_form.is_valid())
        self.client.post(reverse('front:mathematical_object_edition', kwargs={'pk': mathematical_object_2.pk}), mathematical_object_form.data, format='json')

        mathematical_object_2.refresh_from_db()
        self.assertEqual(mathematical_object_2.get_content(), new_description)

    def __create_test_data(self, with_description=None):
        utils.log_as(self, utils.UserType.STAFF)
        func = utils.create_function(self)
        name = utils.create_name(self)
        mathematical_object_1 = utils.create_mathematical_object(self)

        representation = 'createtestdata'
        object_type = 'S'

        data = {
            'latex': representation,
            'type': object_type,
            'functions': [func.id],
            'names': [name.id],
            'related': [mathematical_object_1.id],
        }
        if with_description:
            data.update({'description': with_description})

        mathematical_object_form = forms.MathematicalObjectForm(data=data)
        self.assertTrue(mathematical_object_form.is_valid())
        self.client.post(reverse('front:mathematical_object_creation'), mathematical_object_form.data,
                                    format='json')
        mathematical_object_2 = models.MathematicalObject.objects.exclude(pk=mathematical_object_1.id).first()
        return [mathematical_object_1, mathematical_object_2], func, name
