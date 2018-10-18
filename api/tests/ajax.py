from rest_framework import status
from rest_framework.test import APITestCase
from django.test import override_settings
from django.urls import reverse
from oems.settings import TEST_MEDIA_ROOT
from api.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class AjaxTests(APITestCase):

    def test_retrieve_function_not_connected(self):
        mathematical_object = utils.create_mathematical_object(self)
        function_object = utils.add_function(self, mathematical_object.id,
                                             function_name='test_retrieve_function' + utils.get_random_characters())

        response = self.client.get(reverse('api:function-autocomplete'), format='json')
        self.assertNotContains(response, function_object.function)

    def test_retrieve_function(self):
        utils.login(self)

        mathematical_object = utils.create_mathematical_object(self)
        function_object = utils.add_function(self, mathematical_object.id, function_name='test_retrieve_function' + utils.get_random_characters())

        response = self.client.get(reverse('api:function-autocomplete'), format='json')
        self.assertContains(response, function_object.function)

    def test_retrieve_multiple_functions(self):
        utils.login(self)

        number_of_functions = 3

        mathematical_object = utils.create_mathematical_object(self)
        function_objects = [utils.add_function(self, mathematical_object.id, function_name='test_retrieve_multiple_functions' + utils.get_random_characters()) for _ in range(number_of_functions)]

        response = self.client.get(reverse('api:function-autocomplete'), format='json')
        for function_object in function_objects:
            self.assertContains(response, function_object.function)

    def test_retrieve_only_part_of_functions(self):
        utils.login(self)

        number_of_functions = 3

        mathematical_object = utils.create_mathematical_object(self)
        function_objects_without_bananas = [utils.add_function(self, mathematical_object.id,
                                                               function_name='test_retrieve_only_part_of_functions' + utils.get_random_characters())
                                            for _ in range(number_of_functions)]
        function_objects_with_bananas = [utils.add_function(self, mathematical_object.id,
                                               function_name='bananas' + utils.get_random_characters())
                            for _ in range(number_of_functions)]

        response = self.client.get(reverse('api:function-autocomplete') + "?q=test", format='json')
        for function_object in function_objects_without_bananas:
            self.assertContains(response, function_object.function)
        for function_object in function_objects_with_bananas:
            self.assertNotContains(response, function_object.function)

        response = self.client.get(reverse('api:function-autocomplete') + "?q=banana", format='json')
        for function_object in function_objects_without_bananas:
            self.assertNotContains(response, function_object.function)
        for function_object in function_objects_with_bananas:
            self.assertContains(response, function_object.function)

    def test_retrieve_name_not_connected(self):
        mathematical_object = utils.create_mathematical_object(self)
        name_object = utils.add_name(self, mathematical_object.id, default_name='test_retrieve_name_not_connected' + utils.get_random_characters())

        response = self.client.get(reverse('api:name-autocomplete'), format='json')
        self.assertNotContains(response, name_object.name)

    def test_retrieve_name(self):
        utils.login(self)

        mathematical_object = utils.create_mathematical_object(self)
        name_object = utils.add_name(self, mathematical_object.id, default_name='test_retrieve_name' + utils.get_random_characters())

        response = self.client.get(reverse('api:name-autocomplete'), format='json')
        self.assertContains(response, name_object.name)

    def test_retrieve_multiple_names(self):
        utils.login(self)

        number_of_names = 3

        mathematical_object = utils.create_mathematical_object(self)
        name_objects = [utils.add_name(self, mathematical_object.id, default_name='test_retrieve_multiple_names' + utils.get_random_characters()) for _ in range(number_of_names)]

        response = self.client.get(reverse('api:name-autocomplete'), format='json')
        for name_object in name_objects:
            self.assertContains(response, name_object.name)

    def test_retrieve_only_part_of_names(self):
        utils.login(self)

        number_of_names = 3

        mathematical_object = utils.create_mathematical_object(self)

        name_objects_without_bananas = [utils.add_name(self, mathematical_object.id,
                                                       default_name='test_retrieve_only_part_of_names' + utils.get_random_characters())
                                        for _ in range(number_of_names)]
        name_objects_with_bananas = [
            utils.add_name(self, mathematical_object.id, default_name='bananas' + utils.get_random_characters()) for _
            in range(number_of_names)]

        response = self.client.get(reverse('api:name-autocomplete') + "?q=test", format='json')
        for name_object in name_objects_without_bananas:
            self.assertContains(response, name_object.name)
        for name_object in name_objects_with_bananas:
            self.assertNotContains(response, name_object.name)

        response = self.client.get(reverse('api:name-autocomplete') + "?q=banana", format='json')
        for name_object in name_objects_without_bananas:
            self.assertNotContains(response, name_object.name)
        for name_object in name_objects_with_bananas:
            self.assertContains(response, name_object.name)

    def test_retrieve_tag_not_connected(self):
        mathematical_object = utils.create_mathematical_object(self)
        tag_object = utils.add_tag(self, mathematical_object.id, default_tag='test_retrieve_tag_not_connected' + utils.get_random_characters())

        response = self.client.get(reverse('api:tag-autocomplete'), format='json')
        self.assertNotContains(response, tag_object.tag)

    def test_retrieve_tag(self):
        utils.login(self)

        mathematical_object = utils.create_mathematical_object(self)
        tag_object = utils.add_tag(self, mathematical_object.id, default_tag='test_retrieve_tag' + utils.get_random_characters())

        response = self.client.get(reverse('api:tag-autocomplete'), format='json')
        self.assertContains(response, tag_object.tag)

    def test_retrieve_multiple_tags(self):
        utils.login(self)

        number_of_tags = 3

        mathematical_object = utils.create_mathematical_object(self)
        tag_objects = [utils.add_tag(self, mathematical_object.id, default_tag='test_retrieve_multiple_tags' + utils.get_random_characters()) for _ in range(number_of_tags)]

        response = self.client.get(reverse('api:tag-autocomplete'), format='json')
        for tag_object in tag_objects:
            self.assertContains(response, tag_object.tag)

    def test_retrieve_only_part_of_tags(self):
        utils.login(self)

        number_of_tags = 3

        mathematical_object = utils.create_mathematical_object(self)

        tag_objects_without_bananas = [utils.add_tag(self, mathematical_object.id,
                                                       default_tag='test_retrieve_only_part_of_tags' + utils.get_random_characters())
                                        for _ in range(number_of_tags)]
        tag_objects_with_bananas = [
            utils.add_tag(self, mathematical_object.id, default_tag='bananas' + utils.get_random_characters()) for _
            in range(number_of_tags)]

        response = self.client.get(reverse('api:tag-autocomplete') + "?q=test", format='json')
        for tag_object in tag_objects_without_bananas:
            self.assertContains(response, tag_object.tag)
        for tag_object in tag_objects_with_bananas:
            self.assertNotContains(response, tag_object.tag)

        response = self.client.get(reverse('api:tag-autocomplete') + "?q=banana", format='json')
        for tag_object in tag_objects_without_bananas:
            self.assertNotContains(response, tag_object.tag)
        for tag_object in tag_objects_with_bananas:
            self.assertContains(response, tag_object.tag)