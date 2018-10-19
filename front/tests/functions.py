from django.test import TestCase, override_settings
from django.urls import reverse
from oems.settings import TEST_MEDIA_ROOT
from front import views
from front.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class FunctionsTests(TestCase):

    def test_spread_on_several_pages(self):
        utils.log_as(self, utils.UserType.STAFF)

        number_of_functions = views.PAGINATION_SIZE * 3 + views.PAGINATION_SIZE // 2
        functions = self.__create_functions(number_of_functions)

        for i in range(number_of_functions // views.PAGINATION_SIZE):
            response = self.client.get(reverse('front:functions') + "?page={}".format(i + 1))

            for f in functions[i * views.PAGINATION_SIZE:min((i + 1) * views.PAGINATION_SIZE, number_of_functions)]:
                self.assertContains(response, reverse('front:function', kwargs={'pk': f.pk}))

    def __create_functions(self, number_of_functions):
        return sorted([utils.create_function(self) for _ in range(number_of_functions)], key=lambda x: x.id)
