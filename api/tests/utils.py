from django.contrib.auth.models import Permission
from django.urls import reverse
from rest_framework import status

from api.models import Function, MathematicalObject, Name, Tag, User

from enum import Enum, auto
import random
import string
import os.path


def get_random_characters(length=5):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def add_function(self, object_pk=None, function_name=None):
    if function_name is None:
        function_data = {
            'function': 'add_function' + get_random_characters()
        }
    else:
        function_data = {
            'function': function_name
        }

    if object_pk is None:
        response = self.client.post(reverse('api:functions'), function_data, format='json')
    else:
        response = self.client.post(reverse('api:mathematical_object_functions', kwargs={'object_pk': object_pk}), function_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    return Function.objects.get(pk=response.data['id'])


def add_name(self, object_pk=None, default_name=None):
    if default_name is None:
        name_data = {
            'name': 'add_function' + get_random_characters()
        }
    else:
        name_data = {
            'name': default_name
        }

    if object_pk is None:
        response = self.client.post(reverse('api:names'), name_data, format='json')
    else:
        response = self.client.post(reverse('api:mathematical_object_names', kwargs={'object_pk': object_pk}),
                                    name_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    return Name.objects.get(pk=response.data['id'])


def add_tag(self, object_pk=None, default_tag=None):
    if default_tag is None:
        tag_data = {
            'tag': 'add_tag' + get_random_characters()
        }
    else:
        tag_data = {
            'tag': default_tag
        }

    if object_pk is None:
        response = self.client.post(reverse('api:tags'), tag_data, format='json')
    else:
        response = self.client.post(reverse('api:mathematical_object_tags', kwargs={'object_pk': object_pk}), tag_data,
                                    format='json')
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


class UserType(Enum):
    STAFF = auto()
    USER = auto()
    VISITOR = auto()


def log_as(self, user_type: UserType):
    name = get_random_characters()
    password = get_random_characters()

    if user_type == UserType.STAFF:
        user = User.objects.create_user(name, 'test@test.com', password)

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

        user.user_permissions.add(add_mathematical_object, change_mathematical_object, delete_mathematical_object,
                                  add_function_object, change_function_object, delete_function_object,
                                  add_name_object, change_name_object, delete_name_object,
                                  add_tag_object, change_tag_object, delete_tag_object)
        user.save()

        self.client.login(username=name, password=password)
        return user
    elif user_type == UserType.USER:
        user = User.objects.create_user(name, 'test@test.com', password)
        self.client.login(username=name, password=password)
        return user
    elif user_type == UserType.VISITOR:
        self.client.logout()
        return None
