from rest_framework import status
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from api import models
from front import forms, views

from enum import Enum, auto
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


def create_mathematical_object(self, with_function=False, with_name=False, with_latex=None, description=None):
    representation = 'cmathobj' + get_random_characters()
    if with_latex:
        representation = with_latex

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


def create_tag(self, object_pk=None, tag=None):
    if tag is None:
        tag_data = {
            'tag': 'create_tag' + get_random_characters()
        }
    else:
        tag_data = {
            'tag': tag
        }

    if object_pk:
        response = self.client.post(reverse('api:mathematical_object_tagss', kwargs={'object_pk': object_pk}), tag_data, format='json')
    else:
        response = self.client.post(reverse('api:tags'), tag_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    return models.Tag.objects.get(pk=response.data['id'])


def create_proposition(self, by_user, content: str=None):
    if content is None:
        content = get_random_characters()

    return models.Proposition.objects.create(
        user=by_user,
        content=content
    )


def is_file(file_path):
    return os.path.isfile(file_path)


class UserType(Enum):
    STAFF = auto()
    USER = auto()
    VISITOR = auto()


def log_as(self, user_type: UserType):
    name = get_random_characters()
    password = get_random_characters()

    if user_type == UserType.STAFF:
        user = models.User.objects.create_user(name, 'test@test.com', password)

        add_mathematical_object = Permission.objects.get(codename='add_mathematicalobject')
        change_mathematical_object = Permission.objects.get(codename='change_mathematicalobject')
        delete_mathematical_object = Permission.objects.get(codename='delete_mathematicalobject')

        add_function_object = Permission.objects.get(codename='add_function')
        change_function_object = Permission.objects.get(codename='change_function')
        delete_function_object = Permission.objects.get(codename='delete_function')

        add_name_object = Permission.objects.get(codename='add_name')
        change_name_object = Permission.objects.get(codename='change_name')
        delete_name_object = Permission.objects.get(codename='delete_name')

        add_tag_object = Permission.objects.get(codename='add_tag')
        change_tag_object = Permission.objects.get(codename='change_tag')
        delete_tag_object = Permission.objects.get(codename='delete_tag')

        add_modification = Permission.objects.get(codename='add_modification')
        change_modification = Permission.objects.get(codename='change_modification')
        delete_modification = Permission.objects.get(codename='delete_modification')

        delete_proposition = Permission.objects.get(codename='delete_proposition')

        user.user_permissions.add(add_mathematical_object, change_mathematical_object, delete_mathematical_object,
                                  add_function_object, change_function_object, delete_function_object,
                                  add_name_object, change_name_object, delete_name_object,
                                  add_tag_object, change_tag_object, delete_tag_object,
                                  add_modification, change_modification, delete_modification, delete_proposition)
        user.save()

        self.client.login(username=name, password=password)
        return user
    elif user_type == UserType.USER:
        user = models.User.objects.create_user(name, 'test@test.com', password)
        self.client.login(username=name, password=password)
        return user
    elif user_type == UserType.VISITOR:
        self.client.logout()
        return None
