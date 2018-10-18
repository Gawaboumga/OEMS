from django.urls import reverse
from rest_framework import status

from api.models import Function, MathematicalObject, Name, Tag, User

import random
import string
import os.path


def get_random_characters(length=5):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def add_function(self, object_pk, function_name=None):
    if function_name is None:
        function_data = {
            'function': 'add_function' + get_random_characters()
        }
    else:
        function_data = {
            'function': function_name
        }

    response = self.client.post(reverse('api:mathematical_object_functions', kwargs={'object_pk': object_pk}), function_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    return Function.objects.get(pk=response.data['id'])


def add_name(self, object_pk, default_name=None):
    if default_name is None:
        name_data = {
            'name': 'add_function' + get_random_characters()
        }
    else:
        name_data = {
            'name': default_name
        }

    response = self.client.post(reverse('api:mathematical_object_names', kwargs={'object_pk': object_pk}), name_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    return Name.objects.get(pk=response.data['id'])


def add_tag(self, object_pk, default_tag=None):
    if default_tag is None:
        tag_data = {
            'tag': 'add_tag' + get_random_characters()
        }
    else:
        tag_data = {
            'tag': default_tag
        }

    response = self.client.post(reverse('api:mathematical_object_tags', kwargs={'object_pk': object_pk}), tag_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    return Tag.objects.get(pk=response.data['id'])


def add_relation(self, object_pk, other_pk):
    relation_data = {
        'id': other_pk
    }

    response = self.client.post(reverse('api:mathematical_object_relations', kwargs={'object_pk': object_pk}), relation_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)


def create_mathematical_object(self, with_function=False, with_name=False, with_tag=False, description=None):
    representation = 'cmathobj{}'.format(get_random_characters())
    type = 'S'

    data = {
        'latex': representation,
        'type': type,
    }

    if with_function:
        function = 'function' + get_random_characters()
        data.update({'functions': [{'function': function}]})
    if with_name:
        name = 'name' + get_random_characters()
        data.update({'names': [{'name': name}]})
    if with_tag:
        tag = 'tag' + get_random_characters()
        data.update({'tags': [{'tag': tag}]})
    if description:
        data.update({'description': description})

    response = self.client.post(reverse('api:mathematical_objects'), data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    return MathematicalObject.objects.get(pk=response.data['id'])


def is_file(file_path):
    return os.path.isfile(file_path)


def login(self):
    name = get_random_characters()
    password = get_random_characters()
    user = User.objects.create_user(name, 'test@test.com', password)
    self.client.login(username=name, password=password)
    return user

