from django.test import TestCase, override_settings
from django.urls import reverse
from oems.settings import TEST_MEDIA_ROOT
from front import forms, views
from front.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class NamesTests(TestCase):

    def test_spread_on_several_pages(self):
        utils.log_as(self, utils.UserType.STAFF)

        number_of_names = views.PAGINATION_SIZE * 3 + views.PAGINATION_SIZE // 2
        names = self.__create_names(number_of_names)

        for i in range(number_of_names // views.PAGINATION_SIZE):
            response = self.client.get(reverse('front:names') + "?page={}".format(i + 1))

            for n in names[i * views.PAGINATION_SIZE:min((i + 1) * views.PAGINATION_SIZE, number_of_names)]:
                self.assertContains(response, reverse('front:name', kwargs={'pk': n.pk}))

    def __create_names(self, number_of_names):
        return sorted([utils.create_name(self) for _ in range(number_of_names)], key=lambda x: x.name.lower())
