from rest_framework.test import APITestCase
from django.test import override_settings
from oems.settings import TEST_MEDIA_ROOT
from api.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class ModelsTests(APITestCase):

    def test_add_description_to_mathematical_object(self):
        mathematical_object = utils.create_mathematical_object(self)
        self.assertFalse(bool(mathematical_object.description))

        content = 'test_add_description_to_mathematical_object'
        mathematical_object.save_content(content)

        self.assertEqual(mathematical_object.get_content(), content)

    def test_replace_description_of_mathematical_object(self):
        old_content = 'old_content'
        mathematical_object = utils.create_mathematical_object(self, description=old_content)
        self.assertTrue(bool(mathematical_object.description))
        self.assertEqual(mathematical_object.get_content(), old_content)

        content = 'test_replace_description_of_mathematical_object'
        mathematical_object.save_content(content)

        self.assertEqual(mathematical_object.get_content(), content)

    def test_automatically_delete_description_of_mathematical_object(self):
        mathematical_object = utils.create_mathematical_object(self, description='Test')

        self.assertTrue(utils.is_file(mathematical_object.description.path))

        mathematical_object.delete()
        self.assertFalse(utils.is_file(mathematical_object.description.path))
