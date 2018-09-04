from rest_framework import status
from django.urls import reverse
from api import models
from front import forms, views

import os.path
import random
import re
import string


def get_random_characters(length=5):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def create_function(self, object_pk=None, function_name=None):
    if function_name is None:
        function_data = {
            'function': 'create_function' + get_random_characters()
        }
    else:
        function_data = {
            'function': function_name
        }

    if object_pk:
        response = self.client.post(reverse('api:mathematical_object_functions', kwargs={'object_pk': object_pk}), function_data, format='json')
    else:
        response = self.client.post(reverse('api:functions'), function_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    return models.Function.objects.get(pk=response.data['id'])


def create_mathematical_object(self, with_function=False, with_name=False, description=None):
    representation = 'create_mathematical_object' + get_random_characters()
    type = 'S'

    data = {
        'latex': representation,
        'type': type,
    }

    if with_function:
        function = create_function(self)
        data.update({'functions': [function.id]})
    if with_name:
        name = create_name(self)
        data.update({'names': [name.id]})
    if description:
        data.update({'description': description})

    mathematical_object_form = forms.MathematicalObjectForm(data=data)
    self.assertTrue(mathematical_object_form.is_valid())
    response = self.client.post(reverse('front:mathematical_object_creation'), data=mathematical_object_form.data,
                                format='json')
    self.assertTrue(status.HTTP_302_FOUND)
    id = re.findall(r'\d+', response.url)[-1]
    return models.MathematicalObject.objects.get(pk=id)


def create_modification(self, mathematical_object, new_description=None):
    if not new_description:
        new_description = 'create_modification' + get_random_characters()

    data = {'new_description': new_description}

    modification_form = forms.ModificationForm(data=data)
    self.assertTrue(modification_form.is_valid())
    response = self.client.post(
        reverse('front:mathematical_object_description_edition', kwargs={'pk': mathematical_object.pk}),
        modification_form.data, format='json')

    import re
    results = re.findall(r'\d+', response.url)
    self.assertEqual(len(results), 1)

    modification_object = models.Modification.objects.get(pk=results[0])
    self.assertRedirects(response, reverse('front:modification', kwargs={'pk': modification_object.pk}))
    self.assertEqual(modification_object.get_content(), new_description)
    return modification_object


def create_name(self, object_pk=None, name=None):
    if name is None:
        name_data = {
            'name': 'create_name' + get_random_characters()
        }
    else:
        name_data = {
            'name': name
        }

    if object_pk:
        response = self.client.post(reverse('api:mathematical_object_names', kwargs={'object_pk': object_pk}), name_data, format='json')
    else:
        response = self.client.post(reverse('api:names'), name_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    return models.Name.objects.get(pk=response.data['id'])


def is_file(file_path):
    return os.path.isfile(file_path)


def login(self):
    name = get_random_characters()
    password = get_random_characters()
    user = models.User.objects.create_user(name, 'test@test.com', password)
    self.client.login(username=name, password=password)
    return user
