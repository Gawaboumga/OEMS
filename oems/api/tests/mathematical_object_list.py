from rest_framework import status
from rest_framework.test import APITestCase
from django.test import override_settings
from django.urls import reverse
from oems.settings import TEST_MEDIA_ROOT
from api.models import Function, MathematicalObject, Name


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class MathematicalObjectListTests(APITestCase):

    def test_create_small_mathematical_object(self):
        representation = 'test'
        type = 'S'

        data = {
            'latex': representation,
            'type': type
        }

        response = self.client.post(reverse('api:mathematical_objects'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MathematicalObject.objects.count(), 1)
        response_data = response.data
        self.assertEqual(representation, response_data['latex'])
        self.assertEqual(type, response_data['type'])
        mathematical_object = MathematicalObject.objects.get(pk=response_data['id'])
        self.assertEqual(mathematical_object.functions.count(), 0)
        self.assertEqual(mathematical_object.names.count(), 0)

    def test_create_partial_mathematical_object_with_function(self):
        representation = 'test'
        type = 'S'
        function = 'function'

        data = {
            'latex': representation,
            'type': type,
            'functions': [{'function': function}]
        }

        response = self.client.post(reverse('api:mathematical_objects'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MathematicalObject.objects.count(), 1)
        response_data = response.data
        self.assertEqual(representation, response_data['latex'])
        self.assertEqual(type, response_data['type'])
        mathematical_object = MathematicalObject.objects.get(pk=response_data['id'])
        self.assertEqual(mathematical_object.functions.count(), 1)
        retrieved_function = Function.objects.get(id__in=mathematical_object.functions.all())
        self.assertEqual(function, retrieved_function.function)
        self.assertEqual(mathematical_object.names.count(), 0)

    def test_create_partial_mathematical_object_with_name(self):
        representation = 'test'
        type = 'S'
        name = 'name'

        data = {
            'latex': representation,
            'type': type,
            'names': [{'name': name}]
        }

        response = self.client.post(reverse('api:mathematical_objects'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MathematicalObject.objects.count(), 1)
        response_data = response.data
        self.assertEqual(representation, response_data['latex'])
        self.assertEqual(type, response_data['type'])
        mathematical_object = MathematicalObject.objects.get(pk=response_data['id'])
        self.assertEqual(mathematical_object.functions.count(), 0)
        self.assertEqual(mathematical_object.names.count(), 1)
        retrieved_name = Name.objects.get(id__in=mathematical_object.names.all())
        self.assertEqual(name, retrieved_name.name)

    def test_create_full_mathematical_object(self):
        representation = 'test'
        type = 'S'
        function = 'function'
        name = 'name'

        data = {
            'latex': representation,
            'type': type,
            'functions': [{'function': function}],
            'names': [{'name': name}]
        }

        response = self.client.post(reverse('api:mathematical_objects'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MathematicalObject.objects.count(), 1)
        response_data = response.data
        self.assertEqual(representation, response_data['latex'])
        self.assertEqual(type, response_data['type'])

        mathematical_object = MathematicalObject.objects.get(pk=response_data['id'])
        self.assertEqual(mathematical_object.functions.count(), 1)
        self.assertEqual(mathematical_object.names.count(), 1)
        retrieved_function = Function.objects.get(id__in=mathematical_object.functions.all())
        self.assertEqual(function, retrieved_function.function)
        retrieved_name = Name.objects.get(id__in=mathematical_object.names.all())
        self.assertEqual(name, retrieved_name.name)

    def test_create_mathematical_object_with_description(self):
        representation = 'test_create_mathematical_object_with_description'
        type = 'S'
        description = 'test_create_mathematical_object_with_description'

        data = {
            'latex': representation,
            'type': type,
            'description': description
        }

        response = self.client.post(reverse('api:mathematical_objects'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MathematicalObject.objects.count(), 1)
        response_data = response.data
        self.assertEqual(representation, response_data['latex'])
        self.assertEqual(type, response_data['type'])
        self.assertEqual(description, response_data['description'])
        mathematical_object = MathematicalObject.objects.get(pk=response_data['id'])
        self.assertEqual(mathematical_object.functions.count(), 0)
        self.assertEqual(mathematical_object.names.count(), 0)

    def test_create_invalid_type_mathematical_object(self):
        representation = 'test'
        type = 'BUG'
        function = 'function'
        name = 'name'

        data = {
            'latex': representation,
            'type': type,
            'functions': [{'function', function}],
            'names': [{'name', name}]
        }

        response = self.client.post(reverse('api:mathematical_objects'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(MathematicalObject.objects.count(), 0)

    def test_get_mathematical_objects(self):
        representation_1 = 'test'
        type_1 = 'S'
        function_1 = 'function'
        name_1 = 'name'

        data_1 = {
            'latex': representation_1,
            'type': type_1,
            'functions': [{'function': function_1}],
            'names': [{'name': name_1}]
        }

        response = self.client.post(reverse('api:mathematical_objects'), data_1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MathematicalObject.objects.count(), 1)

        representation_2 = 'test'
        type_2 = 'S'
        function_2 = 'function'
        name_2 = 'name'

        data_2 = {
            'latex': representation_2,
            'type': type_2,
            'functions': [{'function': function_2}],
            'names': [{'name': name_2}]
        }

        response = self.client.post(reverse('api:mathematical_objects'), data_2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MathematicalObject.objects.count(), 2)

        response = self.client.get(reverse('api:mathematical_objects'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_paginated_mathematical_objects(self):
        number_of_objects_to_create = 50
        for i in range(number_of_objects_to_create):
            representation = 'test'
            type = 'S'
            function = 'function'
            name = 'name'

            data = {
                'latex': representation,
                'type': type,
                'functions': [{'function': function}],
                'names': [{'name': name}]
            }

            response = self.client.post(reverse('api:mathematical_objects'), data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(MathematicalObject.objects.count(), i + 1)

        response = self.client.get(reverse('api:mathematical_objects'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(MathematicalObject.objects.count(), number_of_objects_to_create)
        self.assertEqual(len(response.data), number_of_objects_to_create)
