from rest_framework import status
from django.test import TestCase, override_settings
from django.urls import reverse
from oems.settings import TEST_MEDIA_ROOT
from api import models
from front import forms, views
from front.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class MathematicalObjectsTests(TestCase):

    def test_show_mathematical_object(self):
        to_show = views.PAGINATION_SIZE // 2
        object_ids = []
        for _ in range(to_show):
            object_ids.append(utils.create_mathematical_object(self, with_name=True, with_function=True).id)

        self.assertTrue(models.MathematicalObject.objects.count(), to_show)

        response = self.client.get(reverse('front:mathematical_objects'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for object_id in object_ids:
            d = reverse('front:mathematical_object', kwargs={'pk': object_id})
            self.assertContains(response, reverse('front:mathematical_object', kwargs={'pk': object_id}))

    def test_spread_on_several_pages(self):
        number_of_mathematical_objects = views.PAGINATION_SIZE * 3 + views.PAGINATION_SIZE // 2
        mathematical_objects = [utils.create_mathematical_object(self) for _ in range(number_of_mathematical_objects)]

        for i in range(number_of_mathematical_objects // views.PAGINATION_SIZE):
            response = self.client.get(reverse('front:mathematical_objects') + "?page={}".format(i + 1))

            for m in mathematical_objects[i * views.PAGINATION_SIZE:min((i + 1) * views.PAGINATION_SIZE, number_of_mathematical_objects)]:
                self.assertContains(response, reverse('front:mathematical_object', kwargs={'pk': m.pk}))
