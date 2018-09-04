from rest_framework import status
from rest_framework.test import APITestCase
from django.test import override_settings
from django.urls import reverse
from oems.settings import TEST_MEDIA_ROOT
from api.models import MathematicalObject


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class MathematicalObjectDetailTests(APITestCase):

    def test_retrieve_small_mathematical_object(self):
        representation = 'test'
        type = 'S'

        data = {
            'latex': representation,
            'type': type,
        }

        response = self.client.post(reverse('api:mathematical_objects'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(reverse('api:mathematical_object', kwargs={'pk': response.data['id']}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.data
        self.assertEqual(representation, response_data['latex'])
        self.assertEqual(type, response_data['type'])

    def test_retrieve_full_mathematical_object(self):
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

        response = self.client.get(reverse('api:mathematical_object', kwargs={'pk': response.data['id']}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.data
        self.assertEqual(representation, response_data['latex'])
        self.assertEqual(type, response_data['type'])
        self.assertEqual(function, response_data['functions'][0]['function'])
        self.assertEqual(name, response_data['names'][0]['name'])

    def test_put_small_mathematical_object(self):
        representation = 'test'
        type = 'S'

        data = {
            'latex': representation,
            'type': type,
        }

        response = self.client.post(reverse('api:mathematical_objects'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_type = 'P'
        data['type'] = new_type
        response = self.client.put(reverse('api:mathematical_object', kwargs={'pk': response.data['id']}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.data
        self.assertEqual(representation, response_data['latex'])
        self.assertEqual(new_type, response_data['type'])

    def test_delete_full_mathematical_object(self):
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

        response = self.client.delete(reverse('api:mathematical_object', kwargs={'pk': response.data['id']}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(MathematicalObject.objects.count(), 0)
